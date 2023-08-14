import streamlit as st
import pandas as pd
import io
import sqlalchemy
from sqlalchemy import create_engine
import plotly.express as px

st.title('Visualizing Data :sunglasses:')
@st.cache_data(experimental_allow_widgets=True)
#uplode data 
def load_data():
    uploaded_file = st.file_uploader("Choose a file")
    filename = uploaded_file.name
    if filename is not None:
        if filename.endswith('.csv'):
            bytes_data = uploaded_file.getvalue() 
            data = pd.read_csv(io.BytesIO(bytes_data))
        elif filename.endswith('.xlsx'):
            data = pd.read_excel(io.BytesIO(bytes_data))

        else:
            #db_conn = "sqlite:///data.db"
            db_conn = st.text_input("Enter database URL") 
            if db_conn is None:
                raise ValueError("Please provide a database connection string.")
            engine = create_engine(db_conn)

            query = "SELECT * FROM your_table_name"
            data = pd.read_sql(query, engine)
        return data
data = load_data()
sample_frac = 0.4
data = data.sample(frac=sample_frac) 

##################
# Reading Data
def Read_data(df):
    st.write(df.head())
    st.write("shape of data is"  ,df.shape)
    st.write(df.describe())

Read_data(data)


##################
def handle_missing(df):
    # Identify cols with missing values
    cols_with_na = [col for col in df.columns if df[col].isnull().any()] 

    for col in cols_with_na:
        # Drop cols if most values are missing
        if df[col].isnull().mean() > 0.6: 
            df.drop(col, axis=1, inplace=True)
        # Impute mean for numerical 
        elif df[col].dtype != 'object':
            imputer = SimpleImputer(strategy='mean')
            df[col] = imputer.fit_transform(df[[col]])
        # Impute mode for categorical
        else:
            df[col] = df[col].fillna(df[col].mode()[0])

    return df
data = handle_missing(data)

##################
@st.cache_data  
def visulizationOfNumerical(df):
    #get numerical features
    numeric_cols = [col for col in df.columns if df[col].dtype != 'O']
    st.title('Visualizing Numerical Data')
    # Scatter plot
    fig = px.scatter(df, x=numeric_cols[2], y= numeric_cols[3])
    st.plotly_chart(fig)

    fig = px.scatter(df, x=numeric_cols[0], y= numeric_cols[4])
    st.plotly_chart(fig)


    fig = px.bar(df, x=numeric_cols[0], y=numeric_cols[-1])

    fig.update_layout( 
        title='Bar Chart',
        xaxis_title=numeric_cols[0], 
        yaxis_title=numeric_cols[-1]
    )

    fig.update_xaxes(type='category') 

    st.plotly_chart(fig)

    # Histogram
    fig = px.histogram(df, x=numeric_cols[0])
    st.plotly_chart(fig) 

    fig = px.histogram(df, x=numeric_cols[3])
    st.plotly_chart(fig)

    # Box plot
    fig = px.box(df, y= numeric_cols[2])
    st.plotly_chart(fig)

    # Violin plot
    fig = px.violin(df, y= numeric_cols[4])
    st.plotly_chart(fig)
    # Violin plot
    fig = px.violin(df, y= numeric_cols[2])
    st.plotly_chart(fig)
   
visulizationOfNumerical(data)

@st.cache_data(experimental_allow_widgets=True)
def visl_categorical(df):
    st.title('Visualizing categorical Data')

    categorical_cols = [col for col in df.columns if df[col].dtype == 'object']
    fig = px.bar(df, values=categorical_cols[-1], names=categorical_cols[0])
    st.plotly_chart(fig)

    fig = px.bar(df, values=categorical_cols[2], names=categorical_cols[0])
    st.plotly_chart(fig)

    fig = px.bar(df, values=categorical_cols[1], names=categorical_cols[0])
    st.fig)

    fig3 = px.strip(df, x= categorical_cols[2], y= categorical_cols[-1])
    st.plotly_chart(fig3)

visl_categorical(data)
