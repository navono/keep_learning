class OcrItem:
    def __init__(self, pos, val):
        self.position = pos
        self.value = val


class XmlProjectItem:
    def __init__(self, project_name, project_no, device_name, design_phase,
                 pic_no, logic_name, date, contract_no='', description='', designer='',
                 checker='',
                 reviewer='', approve='',
                 ):
        self.project_name = project_name
        self.project_no = project_no
        self.device_name = device_name
        self.design_phase = design_phase
        self.contract_no = contract_no
        self.pic_no = pic_no
        self.logic_name = logic_name
        self.description = description
        self.designer = designer
        self.checker = checker
        self.reviewer = reviewer
        self.approve = approve
        self.date = date
