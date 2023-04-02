import gradio as gr
import cv2
import numpy as np
import random
import os


# 角色颜色生成器
def RGB_to_Hex(rgb):
    color = "#"
    for i in rgb:
        num = int(i)
        color += str(hex(num))[-2:].replace("x", "0").upper()
    return color


def random_color(lightin=True):
    return (
        random.randint(0, 127) + int(lightin) * 128,
        random.randint(0, 127) + int(lightin) * 128,
        random.randint(0, 127) + int(lightin) * 128,
    )


def switch_color(color_style):
    global is_light
    if color_style == "浅色":
        is_light = True
    elif color_style == "深色":
        is_light = False
    back_color_ = random_color(is_light)
    back_color = RGB_to_Hex(back_color_)

    w, h = 50, 50
    img = np.zeros((h, w, 3), np.uint8)
    cv2.rectangle(img, (0, 0), (w, h), back_color_, thickness=-1)

    return back_color, back_color, img


inputs = [gr.Radio(["浅色", "深色"], value="浅色")]

outputs = [
    gr.ColorPicker(label="颜色"),
    gr.Textbox(label="十六进制颜色"),
    gr.Image(type="numpy", label="颜色预览"),
]

title0 = "角色颜色生成器"
description = (
    "点击 Submit 按钮, 生成浅色和深色"
)

tts_demo = gr.Interface(
    fn=switch_color,
    inputs=inputs,
    outputs=outputs,
    title=title0,
    description=description,
)

# renpy代码生成器
title1 = "RenPy代码生成"
description1 = (
    "点击 Submit 按钮，生成RenPy代码"
)


def function(name):
    return f"\" {name}\""


def function1(name):
    return f"\"「{name}」\""


greeter_1 = gr.Interface(fn=function, inputs="textbox", outputs=gr.Textbox(label="对白"))
greeter_2 = gr.Interface(function1, inputs="textbox", outputs=gr.Textbox(label="对话"))

stt_demo = gr.Parallel(greeter_1, greeter_2, title=title1, description=description1)


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
        os.rename(os.path.join(path, file), os.path.join(path, str(num)) + ".jpg")
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
demo = gr.TabbedInterface([tts_demo, stt_demo, pmt_demo, pmp_demo, file_demo], ["color", "code", "tag", "prompt", "file"])
demo.launch()
