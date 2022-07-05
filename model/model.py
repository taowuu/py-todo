class Model(object):
    # all
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def instan_from_dict(cls, d):
        # 因为子元素的 __init__ 需要一个 form 参数
        # 所以这个给一个空字典
        m = cls({})
        for k, v in d.items():
            setattr(m, k, v)
        return m

    @classmethod
    def all(cls):
        path = cls.db_path()
        from utils import load_from_db
        dicts = load_from_db(path)
        ms = [cls.instan_from_dict(d) for d in dicts]
        return ms


    # save
    def append_model(self, models):
        if len(models) == 0:
            self.id = 1
        else:
            m = models[-1]
            self.id = m.id + 1
        models.append(self)

    def replace_model(self, models):
        index = -1
        for i, m in enumerate(models):
            if m.id == self.id:
                index = i
                break
        models[index] = self

    def save(self):
        models = self.all()
        # 如果没有 id，说明是新添加的元素
        if self.id is None:
            self.append_model(models)
        # 有 id 则找到数据对应位置并替换
        else:
            self.replace_model(models)
        #
        l = [m.__dict__ for m in models]
        path = self.db_path()
        from utils import save_to_db
        save_to_db(l, path)


    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def find_by(cls, **kwargs):
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            # 也可以用 getattr(m, k) 取值
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find_all(cls, **kwargs):
        ms = []
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            # 也可以用 getattr(m, k) 取值
            if v == m.__dict__[k]:
                ms.append(m)
        return ms

    def dict_form(self):
        d = self.__dict__.copy()
        return d

    @classmethod
    def delete(cls, id):
        models = cls.all()
        from utils import find_index
        index = find_index(models, id)
        if index is not -1:
            obj = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            from utils import save_to_db
            save_to_db(l, path)
            return obj

    @classmethod
    def update(cls, id, form):
        t = cls.find_by(id=id)
        valid_names = [
            'title'
        ]
        for key in form:
            if key in valid_names:
                setattr(t, key, form[key])
        t.save()
        return t

    def __repr__(self):
        # print(u) 实际上是 print(u.__repr__())
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)
