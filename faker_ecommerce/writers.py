"""
Data writers for PostgreSQL and Parquet output formats.
"""

import os
import pandas as pd


class DataWriter:
    """Abstraction for writing data to PostgreSQL or Parquet files."""
    
    def __init__(self, output_type: str, engine=None, parquet_dir: str = None):
        """
        Initialize the DataWriter.
        
        Args:
            output_type: Either 'postgres' or 'parquet'
            engine: SQLAlchemy engine (required for postgres)
            parquet_dir: Directory path for parquet files (required for parquet)
        """
        self.output_type = output_type
        self.engine = engine
        self.parquet_dir = parquet_dir
        self.table_first_write = {}  # Track first write per table
        
        if output_type == 'parquet' and parquet_dir:
            os.makedirs(parquet_dir, exist_ok=True)
    
    def write_batch(self, table_name: str, data: list) -> int:
        """
        Write a batch of data to the destination.
        
        Args:
            table_name: Name of the table/file
            data: List of dictionaries containing the data
            
        Returns:
            Number of rows written
        """
        if not data:
            return 0
        
        df = pd.DataFrame(data)
        
        if self.output_type == 'postgres':
            is_first = table_name not in self.table_first_write
            if_exists = 'replace' if is_first else 'append'
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            self.table_first_write[table_name] = True
        else:  # parquet
            file_path = os.path.join(self.parquet_dir, f"{table_name}.parquet")
            if table_name not in self.table_first_write:
                # First write - create new file
                df.to_parquet(file_path, index=False, engine='pyarrow')
                self.table_first_write[table_name] = True
            else:
                # Append to existing file
                existing_df = pd.read_parquet(file_path)
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                combined_df.to_parquet(file_path, index=False, engine='pyarrow')
        
        return len(df)
    
    def write_dataframe(self, table_name: str, df: pd.DataFrame) -> int:
        """
        Write a complete DataFrame to the destination.
        
        Args:
            table_name: Name of the table/file
            df: DataFrame to write
            
        Returns:
            Number of rows written
        """
        if self.output_type == 'postgres':
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
        else:  # parquet
            file_path = os.path.join(self.parquet_dir, f"{table_name}.parquet")
            df.to_parquet(file_path, index=False, engine='pyarrow')
        
        self.table_first_write[table_name] = True
        return len(df)

