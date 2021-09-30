#!/usr/bin/env python3
# Created by xiazeng on 2019-06-03
import json
import os.path
import sys
import glob
import shutil
import time


def formatTimeFromTimestamp(format, seconds):
    # 如果format有中文，会有问题，作转码处理
    s = str(format.encode("utf-8"))
    rtn = time.strftime(s, time.localtime(seconds))
    return eval(rtn).decode("utf-8")


ONE_DAY = 86400
ONE_HOUR = 3600
ONE_MIN = 60


def formatCostTime(seconds):
    if seconds > ONE_DAY:
        days = int(seconds / ONE_DAY)
        return "%d天" % days + formatTimeFromTimestamp("%H小时%M分钟%S秒", seconds % ONE_DAY)
    elif seconds > ONE_HOUR:
        return formatTimeFromTimestamp("%H小时%M分钟%S秒", seconds)
    elif seconds > ONE_MIN:
        return formatTimeFromTimestamp("%M分钟%S秒", seconds)
    else:
        return "%.3f秒" % seconds


def generate_meta(outputs):
    filenames = glob.glob(os.path.join(outputs, "*", "*", "*.json"))
    if not filenames:
        return False
    # case datas
    case_datas = []
    for filename in filenames:
        relative_path = os.path.sep.join(filename.split(os.path.sep)[-3:-1])
        m = json.load(open(filename, "rb"))
        m["relative"] = relative_path
        # 查找同目录下 perfdata.json 和 fpsdata.json
        perf_filename = os.path.join(os.path.dirname(filename), "perfdata.json")
        fps_filename = os.path.join(os.path.dirname(filename), "fpsdata.json")
        if os.path.isfile(perf_filename):
            perf = json.load(open(perf_filename, "rb"))
            m["performance"] = perf
        if os.path.isfile(fps_filename):
            fps = json.load(open(fps_filename, "rb"))
            m["fps"] = fps
        case_datas.append(m)
    case_datas.sort(key=lambda a: a["start_timestamp"])

    # summary
    success = 0
    failed = 0
    error = 0
    costs = 0
    pkg_info = {}
    detail = []
    start_time = None
    end_time = None
    for c in case_datas:
        c["costs"] = formatCostTime(c.get("stop_timestamp", c["start_timestamp"]) - c["start_timestamp"])
        if c["success"]:
            success += 1
        elif c["is_failure"]:
            failed += 1
        elif c["is_error"]:
            error += 1
        start_time = (
            c["start_timestamp"]
            if start_time is None
            else min(c["start_timestamp"], start_time)
        )
        end_time = (
            c.get("stop_timestamp", c["start_timestamp"])
            if end_time is None
            else max(c.get("stop_timestamp", c["start_timestamp"]), end_time)
        )
        costs = end_time - start_time
        if c.get("package"):
            if c["package"] in pkg_info:
                pkg_info[c["package"]]["case_num"] += 1
                if c["success"]:
                    pkg_info[c["package"]]["success"] += 1
                elif c["is_failure"]:
                    pkg_info[c["package"]]["failed"] += 1
                elif c["is_error"]:
                    pkg_info[c["package"]]["error"] += 1
                pkg_info[c["package"]]["start_time"] = min(
                    c["start_timestamp"], pkg_info[c["package"]]["start_time"]
                )
                pkg_info[c["package"]]["end_time"] = max(
                    c.get("stop_timestamp", c["start_timestamp"]), pkg_info[c["package"]]["end_time"]
                )
                pkg_info[c["package"]]["costs"] = (
                    pkg_info[c["package"]]["end_time"]
                    - pkg_info[c["package"]]["start_time"]
                )
            else:
                pkg_info[c["package"]] = {
                    "name": c["package"],
                    "case_num": 1,
                    "success": 1 if c["success"] else 0,
                    "failed": 1 if c["is_failure"] else 0,
                    "error": 1 if c["is_error"] else 0,
                    "start_time": c["start_timestamp"],
                    "end_time": c.get("stop_timestamp", c["start_timestamp"]),
                    "costs": c.get("stop_timestamp", c["start_timestamp"]) - c["start_timestamp"],
                }
    for package in pkg_info:
        pkg_info[package]["start_time"] = formatTimeFromTimestamp(
            "%Y/%m/%d %H:%M:%S", pkg_info[package]["start_time"]
        )
        pkg_info[package]["end_time"] = formatTimeFromTimestamp(
            "%Y/%m/%d %H:%M:%S", pkg_info[package]["end_time"]
        )
        pkg_info[package]["costs"] = formatCostTime(pkg_info[package]["costs"])
        detail.append(pkg_info[package])
    detail.sort(key=lambda a: a["start_time"])
    summary = {
        "case_num": len(case_datas),
        "success": success,
        "failed": failed,
        "error": error,
        "costs": formatCostTime(costs),
        "start_time": formatTimeFromTimestamp("%Y/%m/%d %H:%M:%S", start_time),
        "end_time": formatTimeFromTimestamp("%Y/%m/%d %H:%M:%S", end_time),
        "detail": detail,
    }
    meta_json = {"case_datas": case_datas, "summary": summary}
    return meta_json


def generate_meta_v2(outputs):
    tasks = glob.glob(os.path.join(outputs, "[0123456789]*"))
    task_datas = []
    for task in tasks:
        task_data = generate_meta(task)
        if not task_data:
            continue
        for case_data in task_data["case_datas"]:
            case_data["relative"] = os.path.join(
                os.path.basename(task), case_data["relative"]
            )
        task_datas.append(task_data)
    task_datas.sort(key=lambda a: a["summary"]["start_time"], reverse=True)

    summary = {}
    meta_json = {"version": 2, "task_datas": task_datas, "summary": summary}
    return meta_json


# meta_json = generate_meta("/Users/mmtest/code/minium/py-sample/outputs")
# json.dump(meta_json, open("meta.json", "w"), indent=4)


def imp_main(input_path, output_path=None):
    if output_path is None:
        output_path = input_path
    if os.path.exists(output_path) and input_path != output_path:
        print("delete ", output_path)
        shutil.rmtree(output_path)
    if input_path != output_path:
        shutil.copytree(input_path, output_path)
    meta_json = generate_meta_v2(output_path)
    json.dump(meta_json, open(os.path.join(output_path, "meta.json"), "w"), indent=4)
    dist_path = os.path.join(os.path.dirname(__file__), "dist")
    for filename in os.listdir(dist_path):
        path = os.path.join(dist_path, filename)
        target = os.path.join(output_path, filename)
        if os.path.exists(target):
            if os.path.isdir(target):
                shutil.rmtree(target)
            else:
                os.remove(target)
        if os.path.isdir(path):
            shutil.copytree(path, target)
        else:
            shutil.copy(path, target)


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "-h":
        print(
            """
Usage: minireport data_path report_output_path\n\n
    data_path: default report data folder is the folder named 'output' in case folder\n
    report_output_path: anyplace you want
            """
        )
        exit(0)
    input_path = sys.argv[1]
    output_path = None
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    return imp_main(input_path, output_path)


if __name__ == "__main__":
    # outputs = "D:/dddd/weixin/miniumtest/miniprogram-demo-test/outputs"
    # meta_json = generate_meta_v2(outputs)
    # print(meta_json)
    main()