"""VisageLab web UI:  streamlit run app.py"""
import os

import cv2
import pandas as pd
import streamlit as st

from visagelab import Settings, evaluate as ev
from visagelab.detection import FaceDetector
from visagelab.enrollment import prepare
from visagelab.gallery import Gallery, clean_name
from visagelab.pipeline import Pipeline
from visagelab.quality import drop_duplicates

st.set_page_config(page_title="VisageLab", page_icon="🧪", layout="wide")

# Streamlit renamed use_container_width -> width="stretch" (v1.50+); support both.
_ver = tuple(int(p) for p in st.__version__.split(".")[:2] if p.isdigit())
STRETCH = {"width": "stretch"} if _ver >= (1, 50) else {"use_container_width": True}
IMG_TYPES = ["jpg", "jpeg", "png", "bmp", "webp"]


@st.cache_resource
def get_detector():
    return FaceDetector()


def decode(upload):
    import numpy as np
    arr = np.frombuffer(upload.getvalue(), np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


# ---------------------------------------------------------------- sidebar
st.sidebar.title("🧪 VisageLab")
data_dir = st.sidebar.text_input("Data folder", "data")
threshold = st.sidebar.slider("Threshold (max distance)", 20, 130, 55,
                              help="LBPH distance: LOWER = closer match. Lower threshold = stricter.")
margin = st.sidebar.slider("Margin (gap to runner-up)", 0, 30, 6,
                           help="Best person must beat the second-best by this much.")
settings = Settings(data_dir=data_dir, threshold=float(threshold), margin=float(margin))

detector = get_detector()
gallery = Gallery(settings)
pipe = Pipeline(settings, detector=detector)

st.title("VisageLab")
t_enroll, t_id, t_eval, t_gallery = st.tabs(["1 · Enroll", "2 · Identify", "3 · Evaluate", "4 · Gallery"])

# ----------------------------------------------------------------- enroll
with t_enroll:
    st.caption("Register a person. 3-5 clear, front-facing photos in different light/angle work best.")
    name = st.text_input("Name", key="en_name")
    note = st.text_input("How was consent given? (stored with the record)", key="en_note",
                         placeholder="e.g. verbal consent, 15 Oct 2026")
    consent = st.checkbox("This person has given consent to be registered.", key="en_consent")
    skip_quality = st.checkbox("Skip the photo quality check (not recommended)", key="en_skipq",
                               help="By default blurry, dark, low-contrast or tiny faces are rejected.")
    ups = st.file_uploader("Upload photos", type=IMG_TYPES, accept_multiple_files=True, key="en_up")
    cam = st.camera_input("…or take a photo", key="en_cam")

    if st.button("Enroll", type="primary", disabled=not (name.strip() and consent)):
        try:
            clean_name(name)
        except ValueError as e:
            st.error(str(e))
        else:
            frames = [(u.name, decode(u)) for u in (ups or [])] + \
                     ([("camera shot", decode(cam))] if cam is not None else [])
            crops, problems = [], []
            for label, f in frames:
                if f is None:
                    problems.append(f"{label}: unreadable image")
                    continue
                cand = prepare(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), detector, settings,
                               check_quality=not skip_quality)
                if cand.accepted:
                    crops.append(cand.crop)
                else:
                    problems.append(f"{label}: {cand.reason}")
            crops, dupes = drop_duplicates(crops, gallery.crops(name), settings.duplicate_tol)
            if dupes:
                problems.append(f"{dupes} photo(s) skipped: identical to one already used")
            if crops:
                gallery.enroll(name, crops, consent=True, note=note)
                pipe.ready = pipe.matcher.ensure(gallery)
                st.success(f"Enrolled {len(crops)} photo(s) for {clean_name(name)}.")
                st.image(crops, width=90)
            for msg in problems:
                st.warning(msg)
            if not crops and not frames:
                st.warning("Add at least one photo.")

# --------------------------------------------------------------- identify
with t_id:
    if not pipe.ready:
        st.info("Nobody is enrolled yet (tab 1).")
    else:
        mode = st.radio("Source", ["Upload photo", "Webcam snapshot"], horizontal=True)
        src = (st.file_uploader("Photo", type=IMG_TYPES, key="id_up") if mode == "Upload photo"
               else st.camera_input("Snapshot", key="id_cam"))
        if src is not None:
            frame = decode(src)
            if frame is None:
                st.error("Could not read that image.")
            else:
                out, reports = pipe.process(frame)
                left, right = st.columns([3, 2])
                left.image(rgb(out), caption="Green = known, orange = unknown", **STRETCH)
                if reports:
                    right.dataframe(pd.DataFrame([{
                        "face": i + 1, "result": r.name or "Unknown",
                        "match strength": f"{r.score:.0%}", "distance": round(r.distance, 1),
                    } for i, r in enumerate(reports)]), hide_index=True, **STRETCH)
                    right.caption(f"distance: lower = closer. threshold {threshold}, margin {margin}.")
                else:
                    right.warning("No face detected. Try a clearer, front-facing photo.")

# --------------------------------------------------------------- evaluate
with t_eval:
    st.caption("Upload many photos of ONE person (or of people who are NOT enrolled) to see "
               "accuracy and find the best threshold. For a whole test set at once use "
               "`python -m visagelab evaluate <folder>`.")
    if not pipe.ready:
        st.info("Nobody is enrolled yet (tab 1).")
    else:
        UNKNOWN = "Unknown (not enrolled)"
        who = st.selectbox("These photos are of…", [UNKNOWN] + list(gallery.people()))
        files = st.file_uploader("Test photos", type=IMG_TYPES, accept_multiple_files=True, key="ev_up")
        if files:
            expected = None if who == UNKNOWN else who
            samples = []
            for f in files:
                img = decode(f)
                if img is None:
                    continue
                samples.append(ev.probe(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), detector,
                                        pipe.matcher, settings, f.name, expected))
            cur = ev.metrics(samples, settings.threshold, settings.margin)
            st.dataframe(pd.DataFrame([{
                "file": s.path, "face found": s.has_face, "closest": s.best_name or "-",
                "distance": None if not s.has_face else round(s.distance, 1),
                "margin": None if s.margin is None else round(s.margin, 1),
                "result": (ev.decide(s, settings.threshold, settings.margin) or "Unknown")
                          if s.has_face else "-",
            } for s in samples]), hide_index=True, **STRETCH)
            if cur["known"] + cur["impostors"]:
                a, b, c, d = st.columns(4)
                a.metric("Accuracy", f"{cur['accuracy']:.0%}")
                b.metric("FRR (genuine rejected/wrong)", f"{cur['FRR']:.0%}")
                c.metric("FAR (impostor accepted)", f"{cur['FAR']:.0%}")
                d.metric("No face", cur["no_face"])
                rows = ev.sweep(samples, settings.margin)
                best = ev.recommend(rows)
                if ev.can_recommend(cur):
                    st.markdown(f"**Accuracy vs threshold**: best here is **{best['threshold']:.0f}** "
                                f"({best['accuracy']:.0%})")
                else:
                    st.markdown("**Accuracy vs threshold**: no recommendation yet. Upload photos of "
                                "enrolled people AND of strangers (\"Unknown\"); with only one kind "
                                "every threshold looks perfect.")
                st.line_chart(pd.DataFrame(rows).set_index("threshold")[["accuracy", "FRR", "FAR"]])
                if cur["known"] + cur["impostors"] < 10:
                    st.caption("⚠️ Few photos: treat this as a rough guide, not a result.")
            else:
                st.warning("No faces detected in the uploaded photos.")

# ---------------------------------------------------------------- gallery
with t_gallery:
    people = gallery.people()
    if not people:
        st.info("Nobody enrolled yet.")
    for pname, count in people.items():
        with st.container(border=True):
            info = gallery.info(pname).get("consent", {})
            top, btn = st.columns([5, 1])
            top.markdown(f"**{pname}** · {count} photo(s)  \nconsent recorded: "
                         f"{info.get('at', 'unknown')} {('· ' + info['note']) if info.get('note') else ''}")
            if btn.button("Delete", key=f"del_{pname}"):
                gallery.remove(pname)
                pipe.matcher.ensure(gallery)
                st.rerun()
            d = os.path.join(settings.gallery_dir, pname)
            thumbs = sorted(os.listdir(d))[:8]
            cols = st.columns(max(1, len(thumbs)))
            for col, fn in zip(cols, thumbs):
                col.image(os.path.join(d, fn), **STRETCH)
