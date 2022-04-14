function stats_bar(stats_data)
    x = transpose(stats_data{:, 1});
    h = height(stats_data);

    y = zeros(h, 2);
    for i = 1:h
        k = [stats_data{i, 2}, stats_data{i, 3}];

        y(i, :) = k;
    end

    bb = bar(y);
    b = set(gca,'XTickLabel',x);
    legend(b, ["Wszystkie", "Trafienia"]);

    xtips1 = bb(1).XEndPoints;
    ytips1 = bb(1).YEndPoints;
    labels1 = string(bb(1).YData);
    text(xtips1,ytips1,labels1,'HorizontalAlignment','center', 'VerticalAlignment','bottom')

    xtips2 = bb(2).XEndPoints;
    ytips2 = bb(2).YEndPoints;
    labels2 = string(bb(2).YData);
    text(xtips2,ytips2,labels2,'HorizontalAlignment','center', 'VerticalAlignment','bottom')
end