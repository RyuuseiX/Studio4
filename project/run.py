import pythainlp as pyt
import Auto_Tag
import Ask_Question

txt = 'กล้วยนำ้ว้า'
# txt = 'เมื่อวานซื้อ"ฟาร์มเฮ้าส์"มา แพงมากเลย"ไอโฟน"ยังถูกกว่า'
# txt = 'ทัมมัยคะแนนผมแย่จังครัชจารย์'
# txt = 'แม่กับน้องกินปลาย่างอยู่หน้าบ้านกัน 2 คน'
tag = []

q = Ask_Question.Ask_Question()
q.add_text(txt)
q.add_manual_tag(tag)

Auto_Tag.auto_tag(q)

q.save()

print('question : ', q.text)
print('token : ', q.token)
print('pos tag : ', q.pos)
print('keyword : ', q.keyword)
print('auto tag : ', q.auto_tag)
print('manual tag : ', q.manual_tag)
print('tagged question : ', q.tagged_question)

