data = ModelData();

data = data.createModel("./sample_data/gender.csv", ...
              "gender");


data.save("./sample_data/model_data.csv");


newData = ModelData();

newData = newData.readCsv("./sample_data/model_data.csv");

asd