import jinja2

def aa():




        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))

        template = env.get_template('Template.html')

        summary = u"这是一些文字"

        # 输出数据表格的代码
        table = u"后面来制作数据表格"

        # 输出图表的代码
        chart = u"后面来制作图片"

        # 导出图片并保存
        # 语法和format类似，‘=’前面是html模板的{{ }}中的变量名，后面是要导入的内容，我喜欢用一样的名字，比较容易识别
        html = template.render(summary=summary, table=table, chart=chart)
        with open('Report.html', 'w') as f:
                f.write(html)

if __name__=="__main__":
        aa()


