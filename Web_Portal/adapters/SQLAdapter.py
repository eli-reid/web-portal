from logging import fatal
from logging import error
from flask_sqlalchemy import Pagination

from sqlalchemy.log import instance_logger
    
class SQLDBAdapter:
    """
        SQLDBAdapter - provides universal database functions 
        with  logging and error catching
    """

    def __init__(self, failed=False, reason_fail='', *args, **kwargs):
        # class error flags 
        self.failed = failed
        self.reason_fail = reason_fail
        
    def add(self)-> object:
        """ 
            adds and commits record to database
            
            return: returns insatance of self
        """
        try:
            self.db.session.add(self)
            self.db.session.commit()
        except Exception as e:
            error(e)
            return self(failed=True, reason_fail = e) 
        return self

    def delete(self)-> object:
        """ 
            deletes and commits record from database
            
            return: returns insatance of self
        """
        try:
            self.db.session.delete(self)
            self.db.session.commit()
        except Exception as e:
            error(e)
            return self(failed=True, reason_fail = e) 
        return self

    def update(self)-> object:
        """ 
            merges and commits record to database
            
            return: returns insatance of self
        """
        try:           
            self.db.session.commit()
        except Exception as e:
            error(e)
            return self(failed=True, reason_fail = e) 
        return self

    @classmethod
    def get_by_keyword(cls, **keyword)-> object:
        """ 
            queries database 
            
            return: returns multiple records
        """
        try:
            return cls.query.filter_by(**keyword)
        except Exception as e:
            error(e)
            return cls(failed=True, reason_fail = e)

    @classmethod
    def get_first(cls, **keyword)-> object:      
        """ 
            queries database 
            
            return: returns single record
        """
        try:
            return cls.get_by_keyword(**keyword).first()
        except Exception as e:
            error(e)
            return cls(failed=True, reason_fail = e)

    @classmethod
    def get_by_id(cls, id)-> object:
        """ 
            queries database 
            
            return: returns single record
        """
        try:
            return cls.query.get(id)
        except Exception as e:
            error(e)
            return cls(failed=True, reason_fail = e) 
    
    @classmethod
    def get_all(cls)-> object:
        """ 
            queries database 
            
            return: returns all records
        """
        try:
            return cls.query.all()
        except Exception as e:
            error(e)
            return cls(failed=True, reason_fail = e)

    @classmethod
    def paginate(cls, page=None, per_page=None, error_out=True, max_per_page=20, order_by=None)-> Pagination:
        """ 
            queries database 
            
            return: returns multiple records Pagination object 
        """
        try:
            if order_by is not None:
                return cls.query.order_by(order_by).paginate(page, per_page, error_out, max_per_page)
            else:
                return cls.query.paginate(page, per_page, error_out, max_per_page)
        except Exception as e:
            error(e)
            return cls(failed=True, reason_fail = e)