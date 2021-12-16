FROM conda/miniconda3
RUN conda install -c conda-forge cartopy && pip install metpy netcdf4
COPY . .
