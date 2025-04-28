from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import glob
import os
import altair as alt


st.set_page_config(page_title="Tweet Trendleri", layout="wide")
st_autorefresh(interval=10000, key="auto_refresh")

#st_autorefresh(interval=500, key="autorefresh")
st.title("📊 Gerçek Zamanlı Tweet Trendleri")



files = sorted(glob.glob("./spark/output/*.parquet"), key=lambda x: os.path.getmtime(x))
if files:
    df = pd.read_parquet(files[-1])
    #st.dataframe(df)

if files:
    # Tüm .parquet dosyalarını birleştir
    df_list = [pd.read_parquet(f) for f in files]
    df = pd.concat(df_list, ignore_index=True)

    # Gerekli kolonlar: word ve count
    if "hashtag" in df.columns and "count" in df.columns:
        df_grouped = df.groupby("hashtag", as_index=False)["count"].sum()
        df_sorted = df_grouped.sort_values("count", ascending=False).head(20)

        # Altair ile bar chart oluşturuyoruz, x ekseni etiketleri yatay (labelAngle=0)
        chart = alt.Chart(df_sorted).mark_bar().encode(
            x=alt.X("hashtag:N", axis=alt.Axis(labelAngle=0, title="Hashtag")),
            y=alt.Y("count:Q", axis=alt.Axis(title="Count"))
        ).properties(
            width=600,
            height=400
        )
        # Her barın içine count değerini yazdırmak için text katmanı
        text = chart.mark_text(
            align='center',
            baseline='middle',
            color='white'
        ).encode(
            text='count:Q'
        )
        
        st.altair_chart(chart + text, use_container_width=True)
    else:
        st.warning("Veri setinde 'hashtag' ve 'count' sütunları bulunamadı.")
else:
    st.info("Henüz veri dosyası oluşmadı. Spark ve Producer çalışıyor mu?")
