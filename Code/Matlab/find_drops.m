img = imread("F:\F\02202025\exp2\Img73263.jpg");
% Display the frame
imshow(img);
hold on;
%%
[centers, radii] = imfindcircles(img, [50, 120], 'ObjectPolarity', 'bright', 'Sensitivity', .96);

%%

% Plot detected circles
if ~isempty(centers)
    viscircles(centers, radii, 'EdgeColor', 'r');
end

hold off;