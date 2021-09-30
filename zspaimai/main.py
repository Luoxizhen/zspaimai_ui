import minium
mini = minium.Minium({
    "project_path": "/Users/yuanyuanhe/WeChatProjects/miniprogram-1", # 小程序项目目录地址
    "dev_tool_path": "/Applications/wechatwebdevtools.app/Contents/MacOS/cli"
    #"dev_tool_path": "path/to/cli"      # 开发者工具cli地址，如果没有修改过默认安装路径可不填此项

})
print(mini.get_system_info())
#
# uri="ws://localhost"
# dev_tool_path=""
# project_path=None
# test_port=None
# show_log=False
# TEST_PORT=9420
# if not test_port:
#     test_port = TEST_PORT
# test_port = str(test_port)
#
#
# # self.uri=uri.join(":").join(test_port
# uri = uri + ':' + test_port
# print(uri)