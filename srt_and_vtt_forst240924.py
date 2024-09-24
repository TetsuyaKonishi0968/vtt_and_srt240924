import streamlit as st
import streamlit.components.v1 as components  # componentsをインポート

# SRTからVTTに変換する関数
def srt_to_vtt(srt_content):
    vtt_content = "WEBVTT\n\n"
    lines = srt_content.strip().split('\n\n')
    for line in lines:
        entry_lines = line.strip().split('\n')
        if len(entry_lines) >= 2:
            timecode = entry_lines[1]
            start, end = timecode.split(' --> ')
            vtt_content += f"{start.replace(',', '.')} --> {end.replace(',', '.')}\n" + '\n'.join(entry_lines[2:]) + '\n\n'
    return vtt_content

# VTTからSRTに変換する関数
def vtt_to_srt(vtt_content):
    srt_content = ""
    entry_number = 1
    lines = vtt_content.strip().split('\n\n')
    for line in lines:
        entry_lines = line.strip().split('\n')
        if len(entry_lines) >= 2 and '-->' in entry_lines[0]:
            timecode = entry_lines[0]
            start, end = timecode.split(' --> ')
            start = start.replace('.', ',')
            end = end.replace('.', ',')
            srt_content += f"{entry_number}\n{start} --> {end}\n" + '\n'.join(entry_lines[1:]) + '\n\n'
            entry_number += 1
    return srt_content

# フォーマットの判別
def detect_subtitle_format(content):
    if content.strip().startswith("WEBVTT"):
        return 'vtt'
    if '-->' in content and ',' in content.split('-->')[0]:
        return 'srt'
    return None

# アプリのインターフェース
st.title("字幕フォーマット変換")

# テキストボックス1（入力）
input_text = st.text_area("ここにVTTまたはSRT形式の字幕テキストをペーストしてください", height=200)

# ファイルアップローダー
uploaded_file = st.file_uploader("または、ファイルをアップロードしてください（VTTまたはSRT形式）", type=['vtt', 'srt'])

# アップロードされたファイルの処理
if uploaded_file is not None:
    input_text = uploaded_file.getvalue().decode("utf-8")  # ファイルの内容をテキストとして読み込む

# ボタン1（変換）
if st.button("変換"):
    if input_text:
        format_type = detect_subtitle_format(input_text)
        
        if format_type == 'vtt':
            output_text = vtt_to_srt(input_text)
            convert = 'srt'
            st.success("VTTからSRTに変換しました。")
        elif format_type == 'srt':
            output_text = srt_to_vtt(input_text)
            convert = 'vtt'
            st.success("SRTからVTTに変換しました。")
        else:
            output_text = "無効なフォーマットです。VTTまたはSRT形式のテキストを入力してください。"
            st.error("フォーマットの判別に失敗しました。")
        
        # テキストボックス2（出力）
        output_text_box = st.text_area("変換結果", value=output_text, height=200)
        
        # クリップボードにコピーするJavaScriptコード
        components.html(f"""
        <style>
            button {{
                margin-bottom: 0px;  /* ボタンの下の余白をなくす */
            }}
        </style>
        <script>
        function copyToClipboard() {{
            var text = `{output_text}`;
            navigator.clipboard.writeText(text).then(function() {{
                alert('クリップボードにコピーしました!');
            }}, function(err) {{
                console.error('クリップボードへのコピーに失敗しました: ', err);
            }});
        }}
        </script>
        <button onclick="copyToClipboard()">変換結果をコピー</button>
        """, height=35)  # 高さを小さく設定

        # ボタン2（コピー）
        # st.write("変換結果をコピーするには、以下のボタンをクリックしてからテキストをコピーしてください。")
        st.download_button("変換結果を保存", output_text, file_name=f"converted_subtitles.{convert}", mime="text/plain")

    else:
        st.warning("まずテキストをペーストしてください。")

