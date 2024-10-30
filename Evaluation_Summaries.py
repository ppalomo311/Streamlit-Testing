import streamlit as st

st.logo(
    image = 'https://www.morganstanley.com/etc.clientlibs/msdotcomr4/clientlibs/clientlib-site/resources/img/logo-black.png',
    icon_image=None
)

st.title("🏡 Compliance Model Monitoring")


from cognition_datalab.evaluations import get_workflows, get_workflow_metadata
from modelMonitoring.src.utils import workflow_to_dataframe, get_comm_count_metrics, get_alert_count_metrics, get_alert_rate_metrics

THRESHOLD = 0.7

# get all workflows
all_workflow_ids = get_workflows()
all_metadata = {x: get_workflow_metadata(x) for x in all_workflow_ids}


all_workflow_data = {}
for workflow_id in all_workflow_ids:
    df = workflow_to_dataframe(workflow_id, THRESHOLD)
    all_workflow_data[workflow_id] = df
    all_metadata[workflow_id]["Alerts"] = df[df.alerted].message_id.nunique()


st.write(f"---------------------------------\n### Communications Totals")
col1, col2, col3, col4 = st.columns(4)
comm_counts = get_comm_count_metrics(all_workflow_ids, all_metadata)

with col1:
    st.metric(**comm_counts[0])
with col2:
    st.metric(**comm_counts[1])
with col3:
    st.metric(**comm_counts[2])
with col4:
    st.metric(**comm_counts[3])


st.write(f"---------------------------------\n### Alert Totals")

col1, col2, col3, col4 = st.columns(4)
alert_counts = get_alert_count_metrics(all_workflow_ids, all_metadata)

with col1:
    st.metric(**alert_counts[0])
with col2:
    st.metric(**alert_counts[1])
with col3:
    st.metric(**alert_counts[2])
with col4:
    st.metric(**alert_counts[3])


st.write(f"---------------------------------\n### Alert Rates")

col1, col2, col3, col4 = st.columns(4)
alert_rates = get_alert_rate_metrics(all_workflow_ids, all_metadata)

with col1:
    st.metric(**alert_rates[0])
with col2:
    st.metric(**alert_rates[1])
with col3:
    st.metric(**alert_rates[2])
with col4:
    st.metric(**alert_rates[3])

# for i, x in enumerate(zip(all_workflow_ids, st.columns(4))):
#     current_quarter = all_metadata[x[0]]["communications"]
#     if i == 0:
#         comms_delta = 0
#     else:
#         previous_quarter = all_metadata[all_workflow_ids[i-1]]["communications"]
#         comms_delta = ((current_quarter - previous_quarter)/current_quarter)*100

#     x[1].metric(
#         label = f"{x[0]}", 
#         value = f"{current_quarter:,}",
#         delta = f"{round(comms_delta):,}%"
#     )


# st.write(f"---------------------------------\n### Alert Totals")

# for i, x in enumerate(zip(all_workflow_ids, st.columns(4))):
#     current_quarter = all_metadata[x[0]]["Alerts"]
#     if i == 0:
#         alert_delta = 0
#     else:
#         previous_quarter = all_metadata[all_workflow_ids[i-1]]["Alerts"]
#         alert_delta = ((current_quarter - previous_quarter)/current_quarter)*100

#     x[1].metric(
#         label = f"{x[0]}", 
#         value = f"{current_quarter:,}",
#         delta = f"{round(alert_delta):,}%"
#     )



# st.write(f"---------------------------------\n### Alert Rates")

# for i, x in enumerate(zip(all_workflow_ids, st.columns(4))):
#     current_quarter_alerts = all_metadata[x[0]]["Alerts"]
#     current_quarter_comms = all_metadata[x[0]]["communications"]
#     current_quarter_alert_rate = (current_quarter_alerts/current_quarter_comms)*100
#     if i == 0:
#         alert_rate_delta = 0
#     else:
#         previous_quarter_alerts = all_metadata[all_workflow_ids[i-1]]["Alerts"]
#         previous_quarter_comms = all_metadata[all_workflow_ids[i-1]]["communications"]
#         previous_quarter_alert_rate = (previous_quarter_alerts/previous_quarter_comms)*100
#         alert_rate_delta = ((current_quarter_alert_rate - previous_quarter_alert_rate)/current_quarter_alert_rate)*100

#     x[1].metric(
#         label = f"{x[0]}", 
#         value = f"{round(current_quarter_alert_rate):,}%",
#         delta = f"{round(alert_rate_delta):,}%"
#     )