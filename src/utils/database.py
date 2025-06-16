"""Database utilities and setup functions."""

import sqlite3
import requests
import ast
from typing import Optional
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool


def get_engine_for_chinook_db():
    """
    Pull SQL file, populate in-memory database, and create engine.

    Downloads the Chinook database SQL script from GitHub and creates an in-memory
    SQLite database populated with the sample data.

    Returns:
        sqlalchemy.engine.Engine: SQLAlchemy engine connected to the in-memory database
    """
    # Download the Chinook database SQL script from the official repository
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    response = requests.get(url)
    sql_script = response.text

    # Create an in-memory SQLite database connection
    # check_same_thread=False allows the connection to be used across threads
    connection = sqlite3.connect(":memory:", check_same_thread=False)

    # Execute the SQL script to populate the database with sample data
    connection.executescript(sql_script)

    # Create and return a SQLAlchemy engine that uses the populated connection
    return create_engine(
        "sqlite://",  # SQLite URL scheme
        creator=lambda: connection,  # Function that returns the database connection
        poolclass=StaticPool,  # Use StaticPool to maintain single connection
        connect_args={"check_same_thread": False},  # Allow cross-thread usage
    )


def setup_database():
    """
    Set up the database and return a SQLDatabase instance.

    Returns:
        SQLDatabase: LangChain SQLDatabase wrapper
    """
    engine = get_engine_for_chinook_db()
    return SQLDatabase(engine)


def get_customer_id_from_identifier(identifier: str, db: SQLDatabase) -> Optional[int]:
    """
    Retrieve Customer ID using an identifier, which can be a customer ID, email, or phone number.

    This function supports three types of identifiers:
    1. Direct customer ID (numeric string)
    2. Phone number (starts with '+')
    3. Email address (contains '@')

    Args:
        identifier (str): The identifier can be customer ID, email, or phone number.
        db (SQLDatabase): Database instance to query

    Returns:
        Optional[int]: The CustomerId if found, otherwise None.
    """
    # Check if identifier is a direct customer ID (numeric)
    if identifier.isdigit():
        return int(identifier)

    # Check if identifier is a phone number (starts with '+')
    elif identifier.startswith("+"):
        query = f"SELECT CustomerId FROM Customer WHERE Phone = '{identifier}';"
        result = db.run(query)
        formatted_result = ast.literal_eval(result)
        if formatted_result:
            return formatted_result[0][0]

    # Check if identifier is an email address (contains '@')
    elif "@" in identifier:
        query = f"SELECT CustomerId FROM Customer WHERE Email = '{identifier}';"
        result = db.run(query)
        formatted_result = ast.literal_eval(result)
        if formatted_result:
            return formatted_result[0][0]

    # Return None if no match found
    return None
