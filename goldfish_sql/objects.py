# from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column, relationship)
# from sqlalchemy import (ForeignKey, String)


# class Base(DeclarativeBase):
#     pass

# class Continent(Base):
#     pass

# class Country(Base):
#     pass

# class Probes(Base):
#     pass

# class MeasurementId(Base):
#     pass

# class Measurement(Base):
#     pass

class RegistryHolder(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        print(cls, name, bases, namespace)
        if not hasattr(cls, 'registry'):
            cls.registry = set()
        else:
            cls.registry.add(cls)

# Define the base class with the RegistryHolder metaclass
class Base(metaclass=RegistryHolder):
    # The base class doesn't need to do anything special here.
    pass

# Example subclasses
class SubClassA(Base):
    def __init__(self):
        self.integer = 1

class SubClassB(Base):
    pass

