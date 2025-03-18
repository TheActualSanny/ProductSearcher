from pydantic import BaseModel, PositiveFloat, field_validator, model_validator

class Product(BaseModel):
    '''
        A Pydantic class which will be used for the
        finalized products. Instead of transforming
        some values directly while parsing,
        this class will have validation.
    '''

    name: str
    price: PositiveFloat
    product_url: str
    site: str

    @field_validator('price', mode = 'before')
    @classmethod
    def validate_price_type(cls, value: str | float) -> float:
        if isinstance(value, str):
            try:
                price = float(value[1:])
            except ValueError:
                try:
                    seperated = value.split()
                    price = float(''.join(seperated[0][1:]))
                except ValueError:
                    price = float(value.split('$')[1])
            return price
        else:
            return value