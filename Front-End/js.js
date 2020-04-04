(function IFEE(global){
    let windowsRows;
    let windowsCols;
    
    const detectHighwayApiUrl = 'https://taip-highway-detection-api.herokuapp.com/api';
    const cnnApiUrl = 'https://taip-cnn-crack-detection-api.herokuapp.com/api';
    const lbpApiUrl = 'https://taip-lbp-api.herokuapp.com/api';
    const vanishingApiUrl = 'https://taip-vanishing-api.herokuapp.com/api';
    const unetApiUrl = 'http://127.0.0.1:8000/api';
    const slidingSize = 128;
    const lineWidth = 4;
    const offset = 2;

    let yVanishingPoint;

    let initialRawBase64;
    let cnnRawBase64;
    let lbpRawBase64;
    let unetRawBase64;

    let gridMatrix;
    let cellsCount;
    let processedCellsCount;

    let highwayPosColor = 'chartreuse';
    let highwayNegColor = 'red';
    let cnnCrackDetected = '#5ADBFF';
    let cnnCrackNotDetected = '#FFDD4A';

    let setClickHandlers = true;
    let currentState = 0;

    function drawSquare(context, x, y, size, color, lineWidth, callback) {
        context.beginPath();
        context.lineWidth = lineWidth;
        context.strokeStyle = color;
        context.rect(x, y, size - lineWidth, size - lineWidth);
        context.stroke();
        
        if (global.$.isFunction(callback)) {
            callback();
        }
    }

    function drawCircle(context, x, y, callback) {
        context.beginPath();
        context.lineWidth = lineWidth;
        context.strokeStyle = '#ffcc00';
        context.arc(x, y, 25, 0, 2 * Math.PI);
        context.stroke();

        if (global.$.isFunction(callback)) {
            callback();
        }
    }

    function contextDrawImage(context, base64img) {
        context.clearRect(0, 0, context.canvas.width, context.canvas.height);

        const image = new Image();
        image.src = base64img

        context.drawImage(image, 0, 0);
    }

    function getSquareWindow(context, x, y, size) {
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = size;
        tempCanvas.height = size;
        
        const tempContext = tempCanvas.getContext('2d');
        const croppedImage = context.getImageData(x, y, size, size);

        tempContext.putImageData(croppedImage, 0, 0);
        croppedBase64 = tempCanvas.toDataURL("image/jpeg");

        return croppedBase64;
    }

    function getCopyOfImage(context) {
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = context.canvas.width;
        tempCanvas.height = context.canvas.height;
        
        const tempContext = tempCanvas.getContext('2d');
        const croppedImage = context.getImageData(0, 0, tempCanvas.width, tempCanvas.height);

        tempContext.putImageData(croppedImage, 0, 0);
        croppedBase64 = tempCanvas.toDataURL("image/jpeg");

        return croppedBase64;
    }

    function post(path, bodyObject, callback) {
        var request = new XMLHttpRequest();

        request.open('POST', path, true);
        request.setRequestHeader('Content-Type', 'application/json');
        request.onload = function(response) {
            callback(response.currentTarget.response);
        };
        request.send(JSON.stringify(bodyObject));
    }

    function showActions() {
        global.$('#canvas').show();
        global.$('#actions').show();
        global.$('#selections').css('display', 'flex');

        global.$('#upload-text').hide();
        global.$('#file-input').hide();
    }

    function showSpinner() {
        global.$('#spinner').show();

        global.$('#overlay').css('background-color', 'hsla(0, 0%, 71%, 0.3)');
        global.$('#overlay').css('cursor', 'default');
    }

    function hideSpinner() {
        global.$('#spinner').hide();
        global.$('#overlay').css('background-color', '');
        global.$('#overlay').css('cursor', 'pointer');
    }

    function slidingWindowCNN(context, size) {
        contextDrawImage(context, initialRawBase64);

        showSpinner();
        
        cellsCount = 0;
        processedCellsCount = 0;
        windowsRows = Math.ceil(context.canvas.height / size);
        windowsCols = Math.ceil(context.canvas.width / size);

        for (let rowIndex = 0; rowIndex < gridMatrix.length; ++rowIndex) {
            for (let colIndex = 0; colIndex < gridMatrix[rowIndex].length; ++colIndex) {
                if (gridMatrix[rowIndex][colIndex].isPartOfHighway === true) {
                    setTimeout(() => {
                        post(cnnApiUrl, {
                            base64img: gridMatrix[rowIndex][colIndex].base64
                        }, function(response) {
                            processedCellsCount++;
                            let color;
                            if (+response === 1) {
                                color = cnnCrackDetected;
                            } else {
                                color = cnnCrackNotDetected;
                            }
                            drawSquare(context, gridMatrix[rowIndex][colIndex].x, gridMatrix[rowIndex][colIndex].y, size, color, lineWidth,  function() {
                                if (processedCellsCount === cellsCount) {
                                    hideSpinner();
                                    cnnRawBase64 = getCopyOfImage(context);
                                }
                            });
                        });
                    }, 0);
                    cellsCount++;    
                }
            }
        }
    }

    function slidingWindow(context, size, startWithX) {
        cellsCount = 0;
        processedCellsCount = 0;
        windowsRows = Math.ceil((context.canvas.height - startWithX) / size);
        windowsCols = Math.ceil(context.canvas.width / size);
        gridMatrix = [];

        for (let rowIndex = 0; rowIndex < windowsRows; ++rowIndex) {
            let rowList = [];
            let windowY = (rowIndex * size) + offset + startWithX;

            for (let colIndex = 0; colIndex < windowsCols; ++colIndex) {
                let windowX = (colIndex * size) + offset;

                let rawWindowBase64 = getSquareWindow(context, windowX, windowY, size);
                let truncatedBase64 = rawWindowBase64.split(',')[1]
                
                let cellObject = {
                    x: windowX,
                    y: windowY,
                    size: size,
                    base64: truncatedBase64,
                    rawBase64: rawWindowBase64
                }

                post(detectHighwayApiUrl, {
                    base64img: truncatedBase64
                }, function(response) {
                    var color;
                    response = 1;
                    if (+response === 1) {
                        color = highwayPosColor;
                        cellObject.isPartOfHighway = true;
                    } else {
                        color = highwayNegColor;
                        cellObject.isPartOfHighway = false;
                    }
                    drawSquare(context, windowX, windowY, size, color, lineWidth,  function() {
                        processedCellsCount++;
                        if (processedCellsCount === cellsCount) {
                            hideSpinner();
                            global.$('#toast-info').toast('show')
                        }
                    });
                });

                rowList.push(cellObject);
                cellsCount++;
            }
            gridMatrix.push(rowList);
        }
    }

    function setOverlaySize(width, height) {
        const overlay = document.getElementById('overlay');
        overlay.style.width = width + 'px';
        overlay.style.height = height + 'px';

        const overlayClickHandler = function(event) {
            if (currentState !== 1) return;

            if (global.$('#spinner').is(":visible")) {
                return;
            }

            let slidingSizeWOffset = slidingSize - (2 * lineWidth);
            let clientColIndex = Math.floor((event.offsetX - offset) / slidingSizeWOffset);
            let clientRowIndex = Math.floor((event.offsetY - offset - yVanishingPoint) / slidingSizeWOffset);
            let cellY = (clientRowIndex * slidingSize) + offset + yVanishingPoint;
            let cellX = (clientColIndex * slidingSize) + offset;
            
            const canvas = document.getElementById('canvas');
            const context = canvas.getContext('2d');
            
            if (gridMatrix[clientRowIndex] === undefined || 
                gridMatrix[clientRowIndex][clientColIndex] === undefined ||
                gridMatrix[clientRowIndex][clientColIndex].isPartOfHighway === undefined) {
                return;
            }
            
            let newColor;
            if (gridMatrix[clientRowIndex][clientColIndex].isPartOfHighway === true) {
                newColor = highwayNegColor;
            } else {
                newColor = highwayPosColor;
            }
            gridMatrix[clientRowIndex][clientColIndex].isPartOfHighway = !gridMatrix[clientRowIndex][clientColIndex].isPartOfHighway;
            
            drawSquare(context, cellX, cellY, slidingSize, newColor, lineWidth);
        }

        if (setClickHandlers === true) {
            overlay.addEventListener('click', overlayClickHandler);
            setClickHandlers = false;
        }
    }

    function detectHighway() {
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        
        setOverlaySize(ctx.canvas.offsetWidth, ctx.canvas.offsetHeight);

        showSpinner();

        slidingWindow(ctx, slidingSize, 0);

        // post(vanishingApiUrl, {
        //     base64img: canvas.toDataURL("image/jpeg").split(',')[1]
        // }, function(response) {
        //     var response = response.split(',');
        //     var responseX = +response[0].split('[')[1];
        //     var responseY = +response[1].split(']')[0];
        //     drawCircle(ctx, responseX, responseY);
            
        //     yVanishingPoint = responseY;

        //     slidingWindow(ctx, slidingSize, responseY);
        // });
    }

    function detectCracksCNN() {
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        
        slidingWindowCNN(ctx, slidingSize);
    }

    function detectCracksUNET() {
        getSelectedImageBase64(function(base64img){
            post(unetApiUrl, {
                base64img: base64img.split(',')[1]
            }, function(response) {
                console.log(response);
                unetRawBase64 = 'data:image/jpeg;base64,' + response.split('"')[1];
                console.log(unetRawBase64);
            });
        });
    }

    function detectCracksLBP() {
        getSelectedImageBase64(function(base64img){
            post(lbpApiUrl, {
                base64img: base64img.split(',')[1]
            }, function(response) {
                lbpRawBase64 = response;
                let responseObject = JSON.parse(response);
                
                $('#results').append('<span>Major crack: ' + responseObject['major_crack'] + '</span>');
                $('#results').append('<span>Minor crack: ' + responseObject['minor_crack'] + '</span>');
                $('#results').append('<span>No crack: ' + responseObject['no_crack'] + '</span>');
            });
        });
    }

    function getSelectedImageBase64(callback) {
        const canvas = document.getElementById('canvas');
        const tempCanvas = document.createElement('canvas');
        // tempCanvas.width = canvas.width();
        // tempCanvas.height = canvas.height();
        tempCanvas.width = canvas.width;
        tempCanvas.height = canvas.height;
        
        const tempContext = tempCanvas.getContext('2d');
        
        let lowestRowIndex = gridMatrix.length - 1;
        let lowestColIndex = gridMatrix[0].length - 1;

        let emptyRowsCount = 0;
        for (let rowIndex = 0; rowIndex < gridMatrix.length; rowIndex++) {
            let negCells = 0;
            for (let colIndex = 0; colIndex < gridMatrix[rowIndex].length; colIndex++) {
                if (gridMatrix[rowIndex][colIndex].isPartOfHighway !== true) {
                    negCells++;
                }                
            }            
            if (negCells === gridMatrix[rowIndex].length) {
                emptyRowsCount++;
            }
        }

        let emptyColsCount = 0;
        for (let colIndex = 0; colIndex < gridMatrix[0].length; colIndex++) {
            let negCells = 0;
            for (let rowIndex = 0; rowIndex < gridMatrix.length; rowIndex++) {
                if (gridMatrix[rowIndex][colIndex].isPartOfHighway !== true) {
                    negCells++;
                }
            }
            if (negCells === gridMatrix.length) {
                emptyColsCount++;
            }
        }
// + offset
        // const finalCanvasWidth = tempCanvas.width - (emptyColsCount * (slidingSize - (2 * lineWidth)));
        // const finalCanvasHeight = tempCanvas.height - (emptyRowsCount * (slidingSize - (2 * lineWidth)));
        const canvasElement = document.querySelector('#canvas');
        // console.log(canvasElement);
        const finalCanvasWidth = canvasElement.width - (emptyColsCount * (slidingSize - (2 * lineWidth)));
        const finalCanvasHeight = canvasElement.height - (emptyRowsCount * (slidingSize - (2 * lineWidth)));
        // console.log('finalCanvasWidth', finalCanvasWidth);
        // console.log('finalCanvasHeight', finalCanvasHeight);

        const finalCanvas = document.createElement('canvas');
        finalCanvas.width = finalCanvasWidth;
        finalCanvas.height = finalCanvasHeight - yVanishingPoint;
        // finalCanvas.width = 1280;
        // finalCanvas.height = 720;

        const finalCanvasContext = finalCanvas.getContext('2d');
        
        // console.log('empty rows:', emptyRowsCount);
        // console.log('empty cols:', emptyColsCount);

        let processedCellsCount = 0;
        let cellsToProcessCount = 0;
        let selectedBase64;

        for (let rowIndex = 0; rowIndex < gridMatrix.length; rowIndex++) {
            for (let colIndex = 0; colIndex < gridMatrix[rowIndex].length; colIndex++) {
                if (gridMatrix[rowIndex][colIndex].isPartOfHighway === true) {
                    if (rowIndex < lowestRowIndex) {
                        lowestRowIndex = rowIndex;
                    }
                    if (colIndex < lowestColIndex) {
                        lowestColIndex = colIndex;
                    }

                    let tempImage = new Image();
                    tempImage.onload = function() {
                        processedCellsCount++;

                        tempContext.drawImage(tempImage, gridMatrix[rowIndex][colIndex].x, gridMatrix[rowIndex][colIndex].y);

                        if (processedCellsCount === cellsToProcessCount) {
                            // console.log(tempCanvas.toDataURL("image/jpeg").split(',')[1]);

                            let finalImageX = (lowestColIndex * slidingSize) + offset;
                            let finalImageY = (lowestRowIndex * slidingSize) + offset + yVanishingPoint;

                            // console.log('finalImageX', finalImageX);
                            // console.log('finalImageY', finalImageY);

                            let croppedFinalImage = tempContext.getImageData(finalImageX, finalImageY, finalCanvasWidth, finalCanvasHeight);

                            finalCanvasContext.putImageData(croppedFinalImage, 0, 0);
                            
                            // console.log(finalCanvas.toDataURL("image/jpeg").split(',')[1]);

                            // console.warn('lowestRowIndex:', lowestRowIndex);
                            // console.warn('lowestColIndex:', lowestColIndex);
                            selectedBase64 = finalCanvas.toDataURL("image/jpeg");
                            callback(selectedBase64);
                        }
                    }
                    tempImage.src = 'data:image/jpeg;base64,' + gridMatrix[rowIndex][colIndex].base64;

                    cellsToProcessCount++;
                }
            }
        }
        
        // selectedBase64 = finalCanvasContext.toDataURL("image/jpeg");

        return selectedBase64;
    }

    global.showCNN = function() {
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');

        contextDrawImage(ctx, cnnRawBase64);
    }

    global.showUNET = function() {
        if (unetRawBase64 === undefined) return;

        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');

        contextDrawImage(ctx, unetRawBase64);
    }

    // global.showLBP = function() {
    //     const canvas = document.getElementById('canvas');
    //     const ctx = canvas.getContext('2d');

    //     contextDrawImage(ctx, lbpRawBase64);
    // }

    global.onSelectFile = function onSelectFile(event) {
        if (event.target.files && event.target.files[0]) {
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            const img = document.getElementById('img');
            
            const reader = new FileReader();
            const image = new Image();
            
            const loadHanlder = function() {
                canvas.width = img.width;
                canvas.height = img.height;

                ctx.drawImage(image, 0, 0);

                showActions();

                // need to remove the loading handler, otherwise a new handler will be added at every fire of event
                img.removeEventListener('load', loadHanlder);
            }

            reader.onload = (event) => { // called once readAsDataURL is completed
                image.src = event.target.result;
                img.src = event.target.result;
                initialRawBase64 = event.target.result;

                img.addEventListener('load', loadHanlder);
            }

            reader.readAsDataURL(event.target.files[0]); // read file as data url
            
            // global.$('#actions button:nth-of-type(2)').children()[1].focus();
        }
    }

    global.onCheckBoxClicked = function(event) {
        let checkbox = event.target.parentNode.childNodes[1].childNodes[1].childNodes[1];
        checkbox.checked = !checkbox.checked;
    }

    global.uploadClicked = function() {
        currentState = 0;
        rawWindowBase64 = null;
        cnnRawBase64 = null;
        lbpRawBase64 = null;
        unetRawBase64 = null;

        const canvas = document.getElementById('canvas');
        const context = canvas.getContext('2d');
        context.clearRect(0, 0, context.canvas.width, context.canvas.height);

        $('#results').css('visibility', 'hidden');
        $('#results span').remove();
        $('#actions button:nth-child(2)').css('visibility', 'visible');
        $('#overlay').css('cursor', 'pointer');

        global.$('nav span').removeClass('active');
        global.$(global.$('nav span')[currentState]).addClass('active');

        global.$('#file-input').trigger('click');
    }

    global.nextStepClicked = function() {
        if (currentState === 3) {
            return;
        }
        
        currentState++;
        global.$('nav span').removeClass('active');
        global.$(global.$('nav span')[currentState]).addClass('active');

        if (currentState === 1) {
            // Highway detection
            detectHighway();
        }

        if (currentState === 2) {
            // Crack detection
            detectCracksCNN();
            // detectCracksUNET();
            // detectCracksLBP();
        }

        if (currentState === 3) {
            // Final result
            $('#results').css('visibility', 'visible');
            $('#actions button:nth-child(2)').css('visibility', 'hidden');
            $('#overlay').css('cursor', 'default');
        }
    }
})(window);