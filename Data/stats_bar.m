function stats_bar(stats_data)
    x = transpose(stats_data{:, 1});
    h = height(stats_data);

    y = zeros(h, 2);
    for i = 1:h
        k = [stats_data{i, 2}, stats_data{i, 3}];

        y(i, :) = k;
    end

    bar(y)
    b = set(gca,'XTickLabel',x);
    legend(b, ["Wszystkie", "Trafienia"]);
end