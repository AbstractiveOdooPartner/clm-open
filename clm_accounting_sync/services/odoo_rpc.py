import logging
import pprint
import xmlrpc.client

_logger = logging.getLogger(__name__)


class OdooRPC:
    def __init__(self, company):
        self.company = company
        self.url = company.odoo_url
        self.db = company.odoo_db
        self.username = company.odoo_username
        self.password = company.odoo_password
        self.uid = company.odoo_uid

    def common_info(self):
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(self.url))
        _logger.debug("Odoo version information %s", pprint.pformat(common.version()))
        return common

    def authenticate(self):
        common = self.common_info()
        uid = common.authenticate(self.db, self.username, self.password, {})
        self.company.odoo_uid = uid
        auth_data = {"db": self.db, "uid": uid, "password": self.password}
        return auth_data

    def objects(self):
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(self.url))
        return models

    def objects_search_read(self, model, domain, fields, limit=0, offset=0):
        obj = self.objects()
        auth_data = self.authenticate()
        try:
            search_read = obj.execute_kw(
                auth_data.get("db"),
                auth_data.get("uid"),
                auth_data.get("password"),
                model,
                "search_read",
                [domain],
                {"fields": fields, "limit": limit, "offset": offset},
            )
            return search_read
        except Exception as e:
            _logger.debug("objects search and read error %s", pprint.pformat(e))
            if e.faultCode == 3:
                self.authenticate()

    def object_create(self, model, fields, context={}):
        obj = self.objects()
        auth_data = self.authenticate()
        try:
            obj_id = obj.execute_kw(
                auth_data.get("db"),
                auth_data.get("uid"),
                auth_data.get("password"),
                model,
                "create",
                [fields],
                {"context": context},
            )
            return obj_id

        except Exception as e:
            _logger.debug("objects create error %s", pprint.pformat(e))
            if e.faultCode and e.faultCode == 3:
                self.authenticate()

    def object_update(self, model, fields, obj_id):
        obj = self.objects()
        auth_data = self.authenticate()
        try:
            updated_obj = obj.execute_kw(
                auth_data.get("db"), auth_data.get("uid"), auth_data.get("password"), model, "write", [[obj_id], fields]
            )
            return updated_obj

        except Exception as e:
            _logger.debug("objects create error %s", pprint.pformat(e))
            if e.faultCode and e.faultCode == 3:
                self.authenticate()
            elif e.faultCode and e.faultCode == 2:
                return None

    def action_execute(self, model, obj_id, odoo_action):
        obj = self.objects()
        auth_data = self.authenticate()
        try:
            updated_obj = obj.execute_kw(
                auth_data.get("db"), auth_data.get("uid"), auth_data.get("password"), model, odoo_action, [[obj_id]]
            )
            return updated_obj

        except Exception as e:
            _logger.debug("objects create error %s", pprint.pformat(e))
            if e.faultCode and e.faultCode == 3:
                self.authenticate()
            elif e.faultCode and e.faultCode == 2:
                return None
