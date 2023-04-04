import gradio as gr
import os



# tag生成
def pmt_sd(style, input_text):
    return f"""masterpiece, best quality, masterpiece,best quality,official art,extremely detailed CG unity 8k 
    wallpaper,{style}{input_text}"""


title2 = "Tag生成"
description2 = (
    "点击 Submit 按钮，生成Tag"
)

pmt_demo = gr.Interface(
    pmt_sd,
    [
        gr.CheckboxGroup(
            ["comic", "real", "corlorful", "artbook", "light", "night", "bright", "animate", "album", "photo", "sketch",
             "science_fiction", "back", "bust", "profile", "guro"
             ],
            label="风格", info="增加风格Tag"
        ),
        gr.Textbox(
            inputs="text", outputs="text", label="描述文本输入", info="提供文本描述"
        )
    ],
    "text",
    title=title2,
    description=description2,
    examples=[
        [["comic", "light"], "school,overlooking the teaching building, the white building is clean, modern and has a "
                             "sense of science and technology"],
        [["corlorful", "animate"], "quiet forest, light through the leaves, halo"]
    ]
)



# Prompt生成
def pmt_chat(style_1, choose_txt, text_num):
    return f"""帮我写一个{style_1}风格的{choose_txt}视觉小说剧本，字数为{text_num}"""


title3 = "Prompt生成"
description3 = (
    "点击 Submit 按钮，生成Prompt"
)

pmp_demo = gr.Interface(
    pmt_chat,
    [
        gr.Dropdown(
            ["魔幻", "玄幻", "写实", "架空", "穿越"], lable="风格", info="选择剧本风格"
        ),
        gr.CheckboxGroup(
            ["校园", "恋爱", "喜剧", "魔法", "都市", "热血", "冒险", "机甲", "日常",
             "美食", "悬疑", "竞技", "体育", "科幻", "侦探", "青春", "古风", "家庭",
             "推理", "恐怖", "泡泡系", "异世界", "伦理"
             ],
            label="内容", info="选择剧本内容"
        ),
        gr.Slider(500, 5000, value=500, label="字数", info="选择字数"),
    ],
    "text",
    title=title3,
    description=description3,
)

# 操作文件
def file_ctl(file_0):
    path = f"{file_0}"
    num = 1
    for file in os.listdir(path):
        os.rename(os.path.join(path, file), os.path.join(path, str(num)) + ".png")
        num = num + 1
    return f"已经完成文件重命名"

title4 = "图片批量重命名"
description4 = (
    "点击 Submit 按钮，批量重命名文件"
)

file_demo = gr.Interface(
    file_ctl,
    [
        gr.Textbox(
            inputs="text", outputs="text", label="路径", info="输入文件路径"
        )
    ],
    "text",
    title=title4,
    description=description4,
)



# 多页面启动
demo = gr.TabbedInterface(([pmt_demo, pmp_demo, file_demo]),
                          ["tag", "prompt", "file"])
demo.launch()
