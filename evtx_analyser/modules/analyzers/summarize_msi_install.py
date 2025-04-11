

def summarize_msi_install(evtx_events):
    return [evtx_events['Raw_EventData'][i][0] for i in range(len(evtx_events.get("TimeCreated"))) if evtx_events['EventID'][i] == "1033"]