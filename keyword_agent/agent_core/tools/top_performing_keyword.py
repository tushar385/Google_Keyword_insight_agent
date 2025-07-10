from langchain.agents import tool
import snowflake.connector

from config.snowflake_config import snowflake_credentials


# -------------------------
# SNOWFLAKE CONNECTION
# -------------------------
conn = snowflake.connector.connect(
    **snowflake_credentials
)



@tool
def top_performing_keyword(vertical_sector: str) -> list:
    """Returns top 5 performing keywords by impressions for a given industry vertical sector."""

    query = f'''
        select distinct KEYWORD from (
            select
            SUBDOMAIN,CUSTOMER_ID,UNIQUE_CUSTOMER_ID,ADVERTISER_NAME,VENDOR_ACCOUNT_ID,VENDOR_ACCOUNT_NAME,CAMPAIGN_NAME,CURRENCY,	VERTICAL_ID,ADGROUP_NAME,ADGROUP_TYPE,KEYWORD,VERTICAL_NAME,VERTICAL_SECTOR,VERTICAL_SUB_SECTOR,CONNECTOR,NETWORK,	BIDDING_STRATEGY,ADVERTISING_CHANNEL_TYPE,MONTH_YR,IMPRESSIONS,CLICKS,SPEND,SPEND_USD,INTERACTIONS,CONVERSIONS
            from recommendation_data_dev.vertical_insights.GOOGLE_ADS_KEYWORD_MONTHLY_SAMPLE
            where vertical_sector = '{vertical_sector}'
            order by impressions limit 5
        )
    '''

    print(f"Executing query:\n{query}")
    
    try:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        keywords = [row[0] for row in rows]
        return keywords
    except Exception as e:
        return [f"Error: {str(e)}"]
    finally:
        cur.close()
