from sqlalchemy import create_engine
from common.base import BaseModel
from common.config import DB_CONNECT_STRING
from models.user_do import UserDO, ChatLogDO

#---init model---
def init_db(engine):
	BaseModel.metadata.create_all(engine)
	print BaseModel.metadata.create_all(engine)


def drop_db(engine):
	BaseModel.metadata.drop_all(engine)

if __name__ == '__main__':
	import sys
	engine = create_engine(DB_CONNECT_STRING, echo=True)
	if len(sys.argv)>1 and sys.argv[1] == 'drop':
		drop_db(engine)
	else:
		print sys.argv[0]
		init_db(engine)