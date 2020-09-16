from jiankang.db import session_text


class JiankangPipeline(object):
    def process_item(self, item, spider):
        # item['create_time'] = item['time']
        # item.pop('time')
        session_text.add(session_text.add_item(**item))
        session_text.commit()
        return item
