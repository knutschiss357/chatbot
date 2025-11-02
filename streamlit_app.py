import streamlit as st
import google.generativeai as genai

# タイトルと説明を表示
st.title("💬 Chatbot")
st.write(
    "これはGoogle Geminiモデルを使用したシンプルなチャットボットです。"
    "このアプリを使用するには、Google Gemini APIキーが必要です。"
    "[こちら](https://aistudio.google.com/app/apikey)から取得できます。"
)

# Gemini APIキーの入力
gemini_api_key = st.text_input("Google Gemini API Key", type="password")

if not gemini_api_key:
    st.info("続行するにはGoogle Gemini APIキーを入力してください。", icon="🗝️")
else:
    # Geminiクライアントを初期化
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])

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

        # Gemini APIを使用して応答を生成
        try:
            response = chat.send_message(prompt)
            assistant_reply = getattr(response, "text", str(response))

            # アシスタントの応答を表示
            with st.chat_message("assistant"):
                st.markdown(assistant_reply)

            # アシスタントの応答を保存
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# サイドバーにリセットボタンを追加
with st.sidebar:
    if st.button("会話をリセット"):
        st.session_state.messages = []
        st.rerun()
