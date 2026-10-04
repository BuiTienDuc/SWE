import html
import time
from pathlib import Path
import streamlit as st
from runner import run_steps
st.set_page_config(page_title='SWE-bench · Demo PASS/FAIL',page_icon='🧪',layout='wide')
st.markdown('''<style>
.stApp{background:#f5f8fc}h1,h2,h3{color:#15364f}.step{padding:16px 20px;margin:12px 0;border-radius:10px;border-left:6px solid;animation:appear .45s ease-out;font-size:20px}.pass{background:#dcfce7;border-color:#16a34a;color:#14532d}.fail{background:#fee2e2;border-color:#dc2626;color:#991b1b}.step b{float:right}.waiting{background:#dbeafe;padding:18px;border-radius:10px;color:#1e40af;font-size:20px}@keyframes appear{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}@media(prefers-reduced-motion:reduce){.step{animation:none}}
</style>''',unsafe_allow_html=True)
st.title('AI sửa lỗi: PASS test đã đủ chưa?')
st.write('**Issue:** divide(a, 0) phải trả về 0. Với mẫu số khác 0, giữ phép chia đúng, kể cả số lẻ và số âm.')
labels={'baseline':'1. Code ban đầu','regression':'2. Patch gây regression','partial':'3. Patch chưa đầy đủ','fixed':'4. Patch đầy đủ'}
c1,c2,c3=st.columns([2,2,1])
patch=c1.selectbox('Chọn bản sửa',list(labels),format_func=labels.get)
expanded=c2.checkbox('Thêm test phân số và số âm')
manual=c2.checkbox('Dừng sau mỗi bước')
speed=c3.slider('Giây / bước',0.0,3.0,1.2,0.2)
key=(patch,expanded,manual)
if st.session_state.get('selection')!=key:
    st.session_state.update(selection=key,events=[],visible=0,error=None)
left,right=st.columns([1,1.2])
with left:
    st.subheader('Repository & patch')
    st.caption('calculator.py — code hiện có trong repository')
    codebox=st.empty();codebox.code((Path(__file__).parent/'calculator.py').read_text(),language='python')
    if patch!='baseline':
        st.caption('Patch chuẩn bị sẵn để minh họa')
        st.code((Path(__file__).parent/'patches'/f'{patch}.diff').read_text(),language='diff')
    st.info('FAIL_TO_PASS: divide(10, 0) == 0\n\nPASS_TO_PASS: divide(10, 2) == 5\n\nTest bổ sung: 7/2 == 3.5 và -7/2 == -3.5')
with right:
    st.subheader('Các bước thực thi')
    start=st.button('▶ Chạy demo',type='primary')
    if manual and st.session_state.events:
        if st.button('⏭ Hiện bước tiếp theo',disabled=st.session_state.visible>=len(st.session_state.events)):
            st.session_state.visible+=1
    area=st.container()
def render(event):
    ok=event['ok'];cls='pass' if ok else 'fail'
    st.markdown(f'<div class="step {cls}">{html.escape(event["title"])}<b>{"PASS" if ok else "FAIL"}</b></div>',unsafe_allow_html=True)
    with st.expander('Xem patch / log Python'):st.code(event['log'],language='text')
    if 'code' in event:codebox.code(event['code'],language='python')
if start:
    st.session_state.update(events=[],visible=0,error=None)
    try:
        with area:
            progress=st.progress(0);waiting=st.empty()
            total=5 if expanded else 4
            for event in run_steps(patch,expanded):
                st.session_state.events.append(event)
                if not manual:
                    waiting.markdown('<div class="waiting">Đang hiển thị bước '+html.escape(event['title'])+'…</div>',unsafe_allow_html=True)
                    if speed:time.sleep(speed)
                    render(event);st.session_state.visible+=1
                progress.progress(len(st.session_state.events)/total)
            waiting.empty()
        if manual:st.session_state.visible=1;st.rerun()
    except Exception as exc:st.session_state.error=str(exc)
else:
    with area:
        for event in st.session_state.events[:st.session_state.visible]:render(event)
with right:
    if st.session_state.error:st.error('Không chạy được: '+st.session_state.error)
    elif st.session_state.events and st.session_state.visible==len(st.session_state.events):
        if all(e['ok'] for e in st.session_state.events):st.success('PASS — đạt tiêu chí bộ test đã chọn')
        else:st.error('FAIL — chưa đạt tiêu chí bộ test đã chọn')
st.divider()
st.caption('Demo sư phạm độc lập: patch chuẩn bị sẵn, git apply và Python unittest chạy thật trên bản sao tạm. Không gọi AI/API và không chạy benchmark SWE-bench hay UTBoost chính thức. Chế độ tự động thêm thời gian hiển thị để trình chiếu.')
with st.expander('Kịch bản trình diễn 4–5 phút'):
    st.markdown('1. Code ban đầu, tắt test bổ sung → FAIL.\n2. Patch gây regression → sửa lỗi mới nhưng hỏng hành vi cũ.\n3. Patch chưa đầy đủ, tắt test bổ sung → PASS.\n4. Giữ patch đó, bật test bổ sung → FAIL.\n5. Patch đầy đủ, bật test bổ sung → PASS.\n\n**Câu hỏi:** “Cả hai nhóm test PASS, vậy bản sửa đã đúng hoàn toàn chưa?”')
