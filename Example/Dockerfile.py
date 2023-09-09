const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000; // You can change this to your desired port

app.use(bodyParser.json());

const pantryData = {};

app.post('/add-item', (req, res) => {
    try {
        const { pantry_id, basket_key, value } = req.body;

        if (pantry_id && basket_key) {
            const pantry = pantryData[pantry_id] || {};
            pantry[basket_key] = value;
            pantryData[pantry_id] = pantry;
            res.status(201).json({ message: 'Item added successfully' });
        } else {
            res.status(400).json({ message: 'Pantry ID and basket key are required' });
        }
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

app.get('/get-item', (req, res) => {
    try {
        const { pantry_id, basket_key } = req.query;

        if (pantry_id && basket_key && pantryData[pantry_id] && pantryData[pantry_id][basket_key]) {
            const value = pantryData[pantry_id][basket_key];
            res.status(200).json({ value });
        } else {
            res.status(404).json({ message: 'Item not found' });
        }
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

app.get('/list-baskets', (req, res) => {
    try {
        const { pantry_id, filter_name } = req.query;

        if (pantry_id in pantryData) {
            const pantry = pantryData[pantry_id];

            if (filter_name) {
                const filteredBaskets = Object.fromEntries(
                    Object.entries(pantry).filter(([k]) => k.includes(filter_name))
                );
                res.status(200).json(filteredBaskets);
            } else {
                res.status(200).json(pantry);
            }
        } else {
            res.status(404).json({ message: 'Pantry not found' });
        }
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

app.put('/update-item', (req, res) => {
    try {
        const { pantry_id, basket_key, new_value } = req.body;

        if (pantry_id && basket_key && new_value) {
            if (pantry_id in pantryData && basket_key in pantryData[pantry_id]) {
                pantryData[pantry_id][basket_key] = new_value;
                res.status(200).json({ message: 'Item updated successfully' });
            } else {
                res.status(404).json({ message: 'Item not found' });
            }
        } else {
            res.status(400).json({ message: 'Pantry ID, basket key, and new value are required' });
        }
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

app.delete('/delete-item', (req, res) => {
    try {
        const { pantry_id, basket_key } = req.query;

        if (pantry_id && basket_key) {
            if (pantry_id in pantryData && basket_key in pantryData[pantry_id]) {
                delete pantryData[pantry_id][basket_key];
                res.status(200).json({ message: 'Item deleted successfully' });
            } else {
                res.status(404).json({ message: 'Item not found' });
            }
        } else {
            res.status(400).json({ message: 'Pantry ID and basket key are required' });
        }
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
