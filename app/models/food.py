from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


recipe_table = Table('recipe', Base.metadata,
    Column("finished_food", Integer, ForeignKey('food.id')),
    Column("ingredient", Integer, ForeignKey('food.id'))
)

class Food(Base):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(Integer, ForeignKey("food_categories.id"))
    type = Column(String)
    subtype = Column(String)

    servings = relationship(
        "ServingSize", back_populates="food",lazy="joined", cascade="all, delete-orphan"
    )
    
    # ingredients = relationship(
    #     "Food",
    #     secondary=recipe_table,
    #     primaryjoin=id==recipe_table.c.finished_food,
    #     secondaryjoin=id==recipe_table.c.ingredient,
    #     backref="parents",
    #     lazy='selectin'
    # )

