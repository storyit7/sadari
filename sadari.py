import streamlit as st
import matplotlib.pyplot as plt
import random
import time

def draw_columns(n_people):
    """
    인원수에 따라 세로 열만 그립니다.
    """
    fig, ax = plt.subplots(figsize=(n_people * 0.8, 3))
    for i in range(n_people):
        ax.plot([i, i], [0, 3], color='black', lw=2)
    ax.set_xlim(-0.5, n_people - 0.5)
    ax.set_ylim(3, 0)
    ax.axis('off')
    return fig

def generate_ladder(n_people, n_rows):
    """
    인원 수와 층 수에 맞게 사다리의 가로줄을 생성합니다.
    연속된 가로선이 생기지 않도록 합니다.
    """
    ladder = []
    for _ in range(n_rows):
        row = [False] * (n_people - 1)
        j = 0
        while j < n_people - 1:
            if random.choice([True, False]):
                row[j] = True
                j += 2  # 연속 가로선 방지
            else:
                j += 1
        ladder.append(row)
    return ladder

def simulate_path(ladder, start):
    """
    시작 열(start, 0-indexed)에서 출발하여 사다리를 따라 내려가는 경로를 (x, y) 좌표 리스트로 반환합니다.
    """
    path = []
    current_col = start
    y = 0
    path.append((current_col, y))
    for row in ladder:
        y_mid = y + 0.5
        path.append((current_col, y_mid))
        if current_col > 0 and row[current_col - 1]:
            current_col -= 1
            path.append((current_col, y_mid))
        elif current_col < len(row) and row[current_col]:
            current_col += 1
            path.append((current_col, y_mid))
        y += 1
        path.append((current_col, y))
    return path

def draw_ladder(ladder, n_people, n_rows, markers=None):
    """
    Matplotlib를 사용하여 사다리 전체(세로열 + 가로줄)와 진행된 참가자들의 마커(원)를 그립니다.
    markers: (x, y, color) 튜플 리스트
    """
    fig, ax = plt.subplots(figsize=(n_people * 0.8, n_rows / 3))
    # 세로줄 그리기
    for i in range(n_people):
        ax.plot([i, i], [0, n_rows], color='black', lw=2)
    # 가로줄 그리기
    for r, row in enumerate(ladder):
        y = r + 0.5
        for i, has_bar in enumerate(row):
            if has_bar:
                ax.plot([i, i+1], [y, y], color='black', lw=2)
    # 마커 그리기
    if markers:
        for (x, y, col) in markers:
            ax.plot(x, y, 'o', markersize=10, color=col)
    ax.set_xlim(-0.5, n_people - 0.5)
    ax.set_ylim(n_rows, 0)
    ax.axis('off')
    return fig

def main():
    st.markdown("<h2 style='text-align: center;'>비주얼 사다리 게임</h2>", unsafe_allow_html=True)
    
    # 인원수 입력 및 참가자 정보 입력
    n_people = st.number_input("인원수를 입력하세요:", min_value=2, value=5, step=1)
    st.subheader("참가자 정보 입력")
    cols = st.columns(n_people)
    names = []
    bets = []
    base_colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    colors = [base_colors[i % len(base_colors)] for i in range(n_people)]
    for i in range(n_people):
        with cols[i]:
            st.markdown(f"<div style='text-align:center; color:{colors[i]}; font-weight:bold;'>{i+1}번 참가자</div>", unsafe_allow_html=True)
            name = st.text_input("이름", value=f"사람{i+1}", key=f"name_{i}")
            bet = st.text_input("내기명", value=f"내기{i+1}", key=f"bet_{i}")
            names.append(name)
            bets.append(bet)
    
    # 게임 시작 버튼을 먼저 표시 (사다리 이미지 위쪽에 위치)
    game_start = st.button("게임 시작", key="start_button")
    
    # 사다리 영역 placeholder 생성 및 초기 세로 열 표시
    ladder_placeholder = st.empty()
    ladder_placeholder.pyplot(draw_columns(n_people))
    
    if game_start:
        n_rows = random.randint(10, 20)
        st.write(f"랜덤 생성된 사다리 층 수: {n_rows}")
        ladder = generate_ladder(n_people, n_rows)
        paths = [simulate_path(ladder, i) for i in range(n_people)]
        finished_markers = []  # 이미 애니메이션이 완료된 참가자들의 최종 위치
        
        # 1번 참가자부터 순차적으로 애니메이션 진행 (원 이동 속도: 0.1초 간격; 기존 0.3초에서 3배 빠름)
        for i in range(n_people):
            current_path = paths[i]
            for pos in current_path:
                markers = finished_markers.copy()
                markers.append((pos[0], pos[1], colors[i]))
                fig = draw_ladder(ladder, n_people, n_rows, markers=markers)
                ladder_placeholder.pyplot(fig)
                time.sleep(0.2)
            finished_markers.append((current_path[-1][0], current_path[-1][1], colors[i]))
        
        # 최종 결과 출력 (1-indexed)
        results = []
        for i, path in enumerate(paths):
            final_col = path[-1][0] + 1
            results.append(f"{names[i]}({bets[i]}): {final_col}번")
        st.success("게임 결과: " + ", ".join(results))

if __name__ == '__main__':
    main()
