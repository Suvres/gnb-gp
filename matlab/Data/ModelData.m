% -------------------------------------------------------
% Klasa pozwala na przygotowanie oraz wczytanie modelu 
% służącego do wykorzystania później w Gaussian Naive Bayes
% oraz Gaussian Naive Bayes optymalizowanym przez Algorytmy Genetyczne
% -------------------------------------------------------
classdef ModelData
    properties(SetAccess=private)
        savepath = "";
        filepath = "";
        model;
        groupBy;
    end
   
    methods      
        % -------------------------------------------------------
        % Metoda tworzy model danych, które mogą służyć
        % późniejszemu wykorzystaniu w metodz klasyfikacji GNB
        % 
        % [ etykieta, średnia, wariancja, kolumna której dotyczy]
        %
        % Zwraca tabelę [group_by, mean, var, col]
        % -------------------------------------------------------
        function obj = createModel(obj, file_path, group_by)
            obj.filepath = file_path;
            obj.groupBy = group_by;

            opts = detectImportOptions(obj.filepath);
            tmp_table = readtable(obj.filepath, opts);
        
            tmp_group_table = grpstats(tmp_table, group_by, ["mean", "var"]);
        
            base_cols = obj.getColumns(tmp_table);
            
            obj.model = obj.createReturnData(base_cols, tmp_group_table);
        end

        % -------------------------------------------------------
        % Metoda wczytuje przetwożone wcześniej dane, które zostały
        % zapisane do pliku csv
        % -------------------------------------------------------
        function obj = readCsv(obj, filepath)
            opts = detectImportOptions(filepath);
            obj.model = readtable(filepath, opts);
            obj.groupBy = cell2table(obj.model.Properties.VariableNames);
            obj.groupBy = string(obj.groupBy{1, 1});

            disp(strcat("Wczytano tabelę zapisaną w :", filepath));
        end

        function save(obj, savepath)
            obj.savepath = savepath;
            writetable(obj.model, obj.savepath)
            disp(strcat("Zapisano dane do: ", obj.savepath));
        end
    end

    methods (Access=private)
        % -------------------------------------------------------
        % Metoda generuje dwie tablice które zawierają potrzebne kolumny, które są
        % potrzebne do generowania danych
        % -------------------------------------------------------
        function base_cols = getColumns(obj, tmp_table)
            base_cols = cell2table(tmp_table.Properties.VariableNames);
        
            % usuwanie pola geoup_by z gender do późniejszej iteracji
            base_cols = base_cols {1, ~strcmp(base_cols {1, :}, obj.groupBy)};
        
            return;
        end


        % -------------------------------------------------------
        % Metoda generuje tabelę z danymi
        % -------------------------------------------------------
        function returnData = createReturnData(obj, base_cols, group_table)
            count = 1;
            mean_data = [];
            var_data = [];
            col_data = {};
            group_by_data = {};

            for i = 1:height(group_table)
                for cell = base_cols
                    col = cell2mat(cell);
                    mean_col = strcat('mean_', col);
                    var_col = strcat('var_', col);

                    mean_data(count) = group_table{i, mean_col};
                    var_data(count) = group_table{i, var_col};
                    group_by_data(count) = group_table{i, obj.groupBy};
                    col_data(count) = cell;

                    count = count + 1;
                end
            end
            
            returnData = struct2table( ...
                struct(obj.groupBy, group_by_data, ...
                       "mean", num2cell(mean_data), ...
                       "var", num2cell(var_data), ...
                       "col", col_data) ...
               );

            return;
        end
    end
end

