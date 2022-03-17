# read ug csv and return 3 lists for each person sorted by action
def create():
    data = []
    for i in range(5):
        df = pd.read_csv(annot_dir+'ug_list.csv')
        for index, row in df.iterrows():
            clip = row[0]
            header = row[1]
            total_frame = str(row[2])
            action_num = str(row[3])
            data.append([clip, header, total_frame, action_num])
    # make dictionaries for each person
    min = {}
    priya = {}
    fadl = {}
    for j in data:
        if row[0] in utils.clips['minsung']:
            try:
                min[row[3]].append(row[1])
            except:
                min[row[3]] = [row[1]]
        elif row[0] in utils.clips['priya']:
            pri.append(data)
        elif row[0] in utils.clips['fadl']:
            fa.append(data)
    return data