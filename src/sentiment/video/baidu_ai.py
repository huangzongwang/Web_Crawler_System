import requests
import json

def parse_sse_events(response):
    """
    生成器：从 SSE 响应中产出 (event_type, data_str) 对
    """
    event = None
    data_lines = []  # 用于收集多行 data（如果需要）
    
    for line in response.iter_lines(decode_unicode=True):
        if line.startswith('event:'):
            event = line[6:].strip()
        elif line.startswith('data:'):
            # 如果可能有跨多行的 data，先收集起来
            data_lines.append(line[5:].strip())
        elif line == '':
            # 空行：事件结束
            if event and data_lines:
                # 合并多行 data（按 SSE 规范，用换行符连接）
                data_str = '\n'.join(data_lines)
                yield event, data_str
            # 重置
            event = None
            data_lines = []
    
    # 流结束时处理最后一个可能没有空行的事件
    if event and data_lines:
        data_str = '\n'.join(data_lines)
        yield event, data_str

# 发送请求（必须启用 stream=True）
additional_messages=[
  {
      "content": "赛乐赛奥利司他怎么退货?",
      "content_type": "text",
      "role": "user",
      "type": "question"
    }]
response=requests.post("https://api.coze.cn/v1/workflows/chat",headers={"Authorization":"Bearer pat_XgOZsl7O8Pt1N9UQLJySJcaQf6drAobzkZ2a38i32PPRqK31SudaGKOY1CtOpyEJ","Content-Type":"application/json"},json={ "stream":True, "workflow_id": "7612488273806835763","additional_messages":additional_messages})

# 遍历事件流
for event_type, data_str in parse_sse_events(response):
    if event_type == 'conversation.message.completed':
        # 解析 data 中的 JSON
        payload = json.loads(data_str)
        # 提取你关心的字段（例如 output 数组）
        if 'output' in json.loads(payload['content']):
            output_list = json.loads(payload['content'])['output']
            for item in output_list:
                print(f"标题: {item['title']}")
                print(f"链接: {item['url']}")
                print(f"摘要: {item['snippet']}")
                print(f"摘要: {item['date']}")
                break
        
        # 如果只需要第一个匹配的事件，可以在此 break
        # 

# # 可选：检查最终 done 事件
# for event_type, data_str in parse_sse_events(response):
#     if event_type == 'done':
#         print("流结束")