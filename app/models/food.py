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
    category_id = Column(Integer, ForeignKey("food_categories.id", ondelete="CASCADE"), nullable=False)
    type = Column(String)
    subtype = Column(String)
    profile_id = Column(Integer, ForeignKey("profile.id", ondelete="CASCADE"))

    servings = relationship(
        "ServingSize", back_populates="food", lazy="joined", cascade="all, delete-orphan"
    )
    category = relationship("FoodCategories", back_populates="food", lazy="joined")
    
    # ingredients = relationship(
    #     "Food",
    #     secondary=recipe_table,
    #     primaryjoin=id==recipe_table.c.finished_food,
    #     secondaryjoin=id==recipe_table.c.ingredient,
    #     backref="parents",
    #     lazy='selectin'
    # )

