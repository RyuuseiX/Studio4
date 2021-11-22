import pythainlp as pyt
import Auto_Tag
import Ask_Question
import Search_Question

# txt = 'กล้วยนำ้ว้า'
# txt = 'เมื่อวานซื้อ"ฟาร์มเฮ้าส์"มา แพงมากเลย"ไอโฟน"ยังถูกกว่า'
# txt = 'ทัมมัยคะแนนผมแย่จังครัชจารย์'
# txt = 'แม่กับน้องกินปลาย่างอยู่หน้าบ้านกัน 2 คน'
# txt = '"กัปตันซึบาสะ"จะจบมั้ย หรือนักเขียนจะตายก่อน'
tag = []

# print('manual tag : ', q.manual_tag)
# q.add_manual_tag(tag)








txt = 'แม่กรนดังมาก'
aq = Ask_Question.Ask_Question()
aq.add_text(txt)
# sq = Search_Question.Search_Question()
# sq.add_text(txt)

# Auto_Tag.auto_tag(sq)
Auto_Tag.auto_tag(aq)

aq.save()
# sq.save()

print('question : ', aq.text)
print('token : ', aq.token)
print('tag : ', aq.auto_tag)
# print('tagged question : ', aq.tagged_question)
print('')
# print('search question : ', sq.text)
# print('token : ', sq.token)
# print('auto tag : ', sq.auto_tag)
# print('tagged question : ', sq.tagged_question)

