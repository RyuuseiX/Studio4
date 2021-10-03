import pythainlp as pyt
import Auto_Tag
import Ask_Question


q = Ask_Question.Ask_Question()
q.add_text('แม่กินข้าวอยู่หน้าบ้านกับน้อง')
q.add_manual_tag(['กินข้าวนอกบ้าน', 'ครอบครัว'])

Auto_Tag.auto_tag(q)



