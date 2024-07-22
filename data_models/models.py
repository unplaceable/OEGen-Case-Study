from datetime import datetime, timezone
from typing import Tuple
import uuid
import json
import ast
import pandas as pd

from pydantic import BaseModel, Field, field_validator
from pydantic_extra_types.coordinate import Longitude, Latitude

from handlers.data.db import Data
from SETTINGS import TECHNOLOGY_TYPES, PIPELINE_STATUS, RAG_STATUS

# Define the CounterpartyModel using Pydantic for data validation
class CounterpartyModel(BaseModel):
    ID: str = Field(default=str(uuid.uuid4()))
    CounterpartyName: str = Field(max_length=100, min_length=1)
    CEO: str = Field(max_length=100)
    Strategy: str = Field(max_length=100)
    PlatformLead: str = Field(max_length=100)
    DealLead: str = Field(max_length=100)
    FinanceLead: str = Field(max_length=100)
    Created: datetime = datetime.now(timezone.utc)
    LastModified: datetime = datetime.now(timezone.utc)

# Define the PipelineModel using Pydantic for data validation
class PipelineModel(BaseModel):
    ID: str = Field(default=str(uuid.uuid4()))
    CounterpartyID: str
    ProjectName: str = Field(max_length=100)
    Long: Longitude
    Lat: Latitude
    Technology: str
    Capacity: float = Field(ge=0)
    ProjectStatus: str
    RTBDate: datetime
    RAGStatus: str
    RAGComment: str = Field(max_length='300')
    Created: datetime = datetime.now(timezone.utc)
    LastModified: datetime = datetime.now(timezone.utc)

    # Validator for Technology field
    @field_validator("Technology")
    def validate_Technology(cls, v):
        assert v in TECHNOLOGY_TYPES
        return v
    
    # Validator for ProjectStatus field
    @field_validator("ProjectStatus")
    def validate_ProjectStatus(cls, v):
        assert v in PIPELINE_STATUS
        return v
    
    # Validator for RAGStatus field
    @field_validator("RAGStatus")
    def validate_RAGStatus(cls, v):
        assert v in RAG_STATUS
        return v

# Define the PipelineAudit model using Pydantic for audit data validation
class PipelineAudit(BaseModel):
    ID: str = Field(default=str(uuid.uuid4()))
    Created: datetime = datetime.now(timezone.utc)
    Data: dict
    PipelineID: str

# Define the InformationPoint using Pydantic for data validation
class InformationPointModel(BaseModel):
    ID: str = Field(default=str(uuid.uuid4()))
    Title: str = Field(max_length=100)
    Description: str = Field(max_length=500)
    Market: str
    Technology: str
    Counterparties: str
    Impact: int = Field(min=0, max=100)
    Likelihood: int = Field(min=0, max=100)
    Rating: int = Field(min=0, max=10000)
    Created: datetime = datetime.now(timezone.utc)
    LastModified: datetime = datetime.now(timezone.utc)

    # Validator for Technology field
    @field_validator("Technology")
    def validate_Technology(cls, v):
        assert v in TECHNOLOGY_TYPES
        return v

# Base entity class for common operations
class BaseEntity:
    def setup(self, data=None):

        model_lookup = {
            'counterparties': CounterpartyModel,
            'pipelines': PipelineModel,
            'information_points': InformationPointModel
        }

        if self.entity_type in model_lookup:
            self.database=Data(self.entity_type)
        else:
            raise Exception(f'Data for {self.entity_type} is not recognised')

        # Load existing data if ID is provided, otherwise create a new record
        if not data:
            self.data = self.get_all()
        elif 'ID' in data:
            self.data = self.get_by_id(data['ID'])
        else:
            self.model = model_lookup[self.entity_type](**data)
            self.data = self.model.model_dump()
            self.create(self.data)

    # Create a new record in the database
    def create(self, new_record):
        self.database.add_record(new_record)
        Audit.add(new_record)

    # Update a record in the database
    def update_record(self, id, data):
        self.record_audit(data)
        pass
    
    # Bulk update records in the database
    def bulk_update(self, df):
        df.loc[:, "LastModified"] = datetime.now(timezone.utc)
        # for row in df:
        #     self.update_record(id, data)
        self.database.bulk_update(df)

    # Retrieve a record by ID from the database
    def get_by_id(self, id):
        return self.database.get_row_by_id(id)
    
    # Retrieve all records from the database
    def get_all(self, return_type='df'):
        return self.database.get_all(return_type=return_type)
    
    # Search records in the database
    def search(self, search_text, return_type='df', include_columns=None, exclude_columns=None):
        return self.database.search(search_text, return_type=return_type, include_columns=include_columns, exclude_columns=exclude_columns)

# Audit class for handling audit logs
class Audit:
    # Add a new audit record
    def add(data):
        audit_record = {
            'ID': str(uuid.uuid4()),
            'Created': datetime.now(timezone.utc),
            'Data': data,
            'EntityID': data['ID'] or ''
        }

        db = Data('audit')
        db.add_record(audit_record)

    # Get the history of an entity by its ID
    def get_history(entity_id):
        db = Data('audit')
        results = db.find(column='EntityID', value=entity_id, return_type='raw', include_columns=['Created', 'Data'])
        return results

# Counterparty entity class
class Counterparty(BaseEntity):
    def __init__(self, data=None):
        self.entity_type = 'counterparties'
        self.setup(data)

# Pipeline entity class
class Pipeline(BaseEntity):
    def __init__(self, data=None):
        self.entity_type = 'pipelines'
        self.setup(data)

        # self.extend_with_counterparty()

    def extend_with_counterparty(self):


        result = pd.merge(self.data, Counterparty().get_all(), how='left', left_on='CounterpartyID', right_on='ID', suffixes=('', '_counterparty'))

        # Drop the duplicate ID column from the second data frame
        self.data = result.drop(columns=['ID_counterparty'])


        return True

class InformationPoint(BaseEntity):
    def __init__(self, data=None):
        self.entity_type = 'information_points'
        if data and 'ID' not in data:
            data['Rating']=self.create_rating(impact=data['Impact'], likelihood=data['Likelihood'])
        self.setup(data)

    def create_rating(self, impact=None, likelihood=None):

        rating = impact * likelihood

        return rating




if __name__ == "__main__":

    data = {'Title': 'New information point is here', 'Description': 'Long description about the information point', 'Market': 'test', 'Technology': 'Solar', 'Counterparties': ['Red Rock Industries', 'Green Energy Corp is the best'], 'Impact': 41, 'Likelihood': 67}

    InformationPoint(data)