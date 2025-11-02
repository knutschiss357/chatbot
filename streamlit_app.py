import streamlit as st
from openai import OpenAI

# タイトルと説明を表示
st.title("💬 Chatbot")
st.write(
    "これはOpenAIのGPT-3.5モデルを使用したシンプルなチャットボットです。"
    "このアプリを使用するには、OpenAI APIキーが必要です。"
    "[こちら](https://platform.openai.com/account/api-keys)から取得できます。"
)

# OpenAI APIキーの入力
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("続行するにはOpenAI APIキーを入力してください。", icon="🗝️")
else:
    # OpenAIクライアントを作成
    client = OpenAI(api_key=openai_api_key)
    
    # セッション状態でチャットメッセージを保存
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # 既存のチャットメッセージを表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # チャット入力フィールド
    if prompt := st.chat_input("メッセージを入力してください"):
        # ユーザーメッセージを保存して表示
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # OpenAI APIを使用して応答を生成
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            
            # ストリーミングレスポンスを表示
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            
            # アシスタントの応答を保存
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            
# サイドバーにリセットボタンを追加
with st.sidebar:
    if st.button("会話をリセット"):
        st.session_state.messages = []
        st.rerun()
