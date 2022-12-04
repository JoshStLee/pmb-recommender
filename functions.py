import streamlit as st
import pandas as pd
import numpy as np

def explore_tree(X, test, rfc, n_nodes, children_left,children_right, feature,threshold,
                suffix='', print_tree= False, sample_id=0):

    node_indicator = rfc.decision_path(test)
    leave_id = rfc.apply(test)
    node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                        node_indicator.indptr[sample_id + 1]]
    
    for node_id in node_index:
    
        tabulation = ""
        if leave_id[sample_id] == node_id:
            break
        if (test.iloc[sample_id, feature[node_id]] <= threshold[node_id]):
            threshold_sign = "<="
        else:
            threshold_sign = ">"

        st.write("%s (= %s) %s %s"
              % (X.columns.values[feature[node_id]],
                 test.iloc[sample_id, feature[node_id]],
                 threshold_sign,
                 threshold[node_id]))
    st.write("\n%sPrediction for submitted data: %s"%(tabulation,
                                                 rfc.predict(test)[sample_id]))


def retrain_ml(X_train, y_train, data_baru, model):
    train_baru = data_baru.drop(['is_diterima'],axis=1)
    class_baru = data_baru[['is_diterima']]
    X_train = pd.concat([X_train,train_baru], ignore_index=True)
    y_train = pd.concat([y_train,class_baru], ignore_index=True)
    model.fit(X_train, y_train)
    st.write("Luaran Dilatih")