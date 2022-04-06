classdef GNBSimple
    properties(Access=private)
        % Jest to równanie wykorzystywane w klasyfikacji
        f_gnb = @(var, mean, x) (1 ./ (sqrt(2 .* pi .* var))) .* exp(-((x - mean).^2) ./ (2 * var)); 
        simpleStats;
    end
    
    properties
        statsTable;
        prior = 0;
    end

    methods
        % -------------------------------------------------------
        % Metoda wyliczająca statystykę trafień dla każdej etykiet
        % dla podstawowej klasyfikacji Bayesa
        % -------------------------------------------------------
        function obj = simpleComputeSampleData(obj, filepath, model_data)
            group_by = string(model_data.Properties.VariableNames{1,1});

            opts = detectImportOptions(filepath);
            sample_data = readtable(filepath, opts);
            
            obj.simpleStats = grpstats(sample_data, group_by, []);
            obj.prior = 1./height(obj.simpleStats);
            obj.statsTable = obj.calculateHitsStats(sample_data, ...
                                                     obj.simpleStats, ...
                                                     model_data, ...
                                                     group_by);
            
        end
    end

    methods (Access=private)
        function statsTable = calculateHitsStats( ...
                obj, ...
                sample_data, ...
                simple_stats, ...
                model_data, ...
                group_by ...
                )
            
            labels = transpose(simple_stats{:, group_by});
            results = zeros(1, size(labels, 2));

            counts = simple_stats{:, 2};

            for i= 1:height(sample_data)
                row = sample_data(i, :);
                search = string(row{1, group_by});
                
                result = obj.computeRow(model_data, row, labels);
                 label_id = find(strcmp(labels(1, :), search));

                if search == result
                    results(label_id) = results(label_id) + 1;
                else
                    results(label_id) = results(label_id);
                end
            end

            statsTable = struct2table(struct( ...
                'Etykieta', labels, ...
                'Wszystkie', num2cell(transpose(counts)), ...
                'Trafienia', num2cell(results) ...
                ));

        end
        
        % -------------------------------------------------------
        % Metoda kalkuluje wiersz danych, oraz zwraca przewidywaną etykietę
        % -------------------------------------------------------
        function result = computeRow(obj, model, row, labels)
            predicts = [];
            results = {};
            
            c = 1;
            for label = labels
                tmp_t = model(strcmp(model{:, 1}, label), :);
                data = zeros(height(tmp_t), 3);

                for i = 1:height(tmp_t)
                    x = row{:, cell2mat(tmp_t{i, "col"})};
                    var = tmp_t{i, 'var'};
                    mean = tmp_t{i, 'mean'};
                    data(i, :) = [var, mean, x];
                end

                predicts(c) = obj.calculatePredict(data);
                results(c) = label;

                c = c + 1;
            end

            result = string(results(predicts == max(predicts)));
        end

        % -------------------------------------------------------
        % Metoda oblicza wartość przewidywania, na ile szukana należy do
        % zbioru
        % -------------------------------------------------------
        function predict = calculatePredict(obj, array)
          predict = obj.prior;
          for l = transpose(array)   
             predict = predict .* obj.f_gnb(l(1), l(2), l(3));
          end
        
        end 

       
    end
end

