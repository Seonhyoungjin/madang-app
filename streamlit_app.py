import streamlit as st

st.set_page_config(page_title="마당서점", page_icon="📚")
st.title("📚 마당서점 구매 내역 조회")
st.caption("고객 이름을 입력하면 그 고객이 구입한 도서를 Neon DB에서 찾아 보여줍니다.")

# Streamlit Secrets의 [connections.neon] 주소로 Neon DB에 접속
conn = st.connection("neon", type="sql")

name = st.text_input("고객 이름", placeholder="예: 박지성")

if name:
    df = conn.query(
        """
        SELECT b.bookname  AS 도서명,
               b.publisher AS 출판사,
               o.saleprice AS 구매가격,
               o.orderdate AS 구매일
        FROM Orders o
        JOIN Customer c ON o.custid = c.custid
        JOIN Book b     ON o.bookid = b.bookid
        WHERE c.name = :name
        ORDER BY o.orderdate;
        """,
        params={"name": name.strip()},
        ttl=0,
    )
    if df.empty:
        st.warning(f"'{name}' 고객의 구매 내역이 없습니다.")
    else:
        st.success(f"{name} 님은 {len(df)}권을 구입했습니다.")
        st.dataframe(df, hide_index=True)
        st.metric("총 구매금액", f"{int(df['구매가격'].sum()):,}원")

with st.expander("전체 고객 명단 보기"):
    st.dataframe(conn.query("SELECT name AS 이름, address AS 주소 FROM Customer ORDER BY custid;", ttl=0),
                 hide_index=True)
