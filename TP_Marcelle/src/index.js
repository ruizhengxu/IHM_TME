import '@marcellejs/core/dist/marcelle.css';
import * as marcelle from '@marcellejs/core';

// Main page //
const input = marcelle.sketchPad();
const featureExtractor = marcelle.mobileNet();

const label = marcelle.textInput();
label.title = 'Text input';
label.$value.subscribe((currentInput) => {
  console.log('currentInput:', currentInput);
});

const capture = marcelle.button('Click to record an instance');
capture.title = 'Capture current drawing instance';

const $instances = capture.$click
  .sample(input.$images)
  .map(async (img) => ({
    x: await featureExtractor.process(img),
    y: label.$value.value,
    thumbnail: input.$thumbnails.value,
  }))
  .awaitPromises();
  

const store = marcelle.dataStore('localStorage');
const trainingSet = marcelle.dataset('TrainingSet', store);

$instances.subscribe(trainingSet.create.bind(trainingSet));

const trainingSetBrowser = marcelle.datasetBrowser(trainingSet);

const classifier = marcelle.mlpClassifier({ layers: [32, 32], epochs: 20 });
const classifier_ = marcelle.mlpClassifier({ layers: [64, 32], epochs: 40 });
const classifier__ = marcelle.mlpClassifier({ layers: [64, 64], epochs: 60 });
const trainingButton = marcelle.button('Train');

trainingButton.$click.subscribe(() => {
  classifier.train(trainingSet);
  classifier_.train(trainingSet);
  classifier__.train(trainingSet);
});

const plotTraining = marcelle.trainingPlot(classifier);

const $predictions = input.$images
  .map(async (img) => {
    const features = await featureExtractor.process(img);
    return classifier.predict(features);
  })
  .awaitPromises();

const predViz = marcelle.confidencePlot($predictions);

const progress = marcelle.trainingProgress(classifier);

const predictButton = marcelle.button('Update Confusion Matrix');
const batchResults = marcelle.batchPrediction({ name: 'mlp', dataStore: store });
const confMat = marcelle.confusionMatrix(batchResults);
predictButton.$click.subscribe(async () => {
  if (!classifier.ready) {
    marcelle.throwError(new Error('No classifier has been trained'));
  }
  await batchResults.clear();
  await batchResults.predict(classifier, trainingSet);
});

// Upload page //
const source = marcelle.imageUpload();

const imgDisplay = marcelle.imageDisplay(source.$images);

const $predictions1 = source.$images
  .map(async (img) => {
    const features = await featureExtractor.process(img);
    if (!classifier.ready) {
      marcelle.throwError(new Error('No classifier has been trained'));
    }
    return classifier.predict(features);
  })
  .awaitPromises();

  const $predictions2 = source.$images
  .map(async (img) => {
    const features = await featureExtractor.process(img);
    return classifier_.predict(features);
  })
  .awaitPromises();

const $predictions3 = source.$images
  .map(async (img) => {
    const features = await featureExtractor.process(img);
    console.log(classifier__.predict(features));
    return classifier__.predict(features);
  })
  .awaitPromises();

// const $predictions4 = source.$images
//   .map(async (img) => {
//     const features = await featureExtractor.process(img);
//     const pred1 = (await classifier.predict(features)).confidences;
//     const pred2 = (await classifier_.predict(features)).confidences
//     const pred3 = (await classifier__.predict(features)).confidences
//     console.log(pred1, pred2, pred3)
//     return pred1 + pred2 + pred3
//   })
//   .awaitPromises();

const predViz1 = marcelle.confidencePlot($predictions1);
predViz1.title = "Prediction MLP [32, 32] with epoch = 20"
const predViz2 = marcelle.confidencePlot($predictions2);
predViz2.title = "Prediction MLP [64, 32] with epoch = 40"
const predViz3 = marcelle.confidencePlot($predictions3);
predViz3.title = "Prediction MLP [64, 64] with epoch = 60"
// const c = marcelle.confusionMatrix();

// Render page //

const dash = marcelle.dashboard({
  title: 'Drawing Recognizer',
  author: 'Ruizheng XU',
});

dash
  .page('Main')
  .sidebar(input, featureExtractor, trainingButton, predictButton)
  .use(predViz, [label, capture], trainingSetBrowser)
  .use(progress)
  .use(confMat)
  .use(plotTraining);

dash
  .page("Upload")
  .sidebar(featureExtractor)
  .use(source, imgDisplay, [predViz1, predViz2, predViz3])

dash.show();
