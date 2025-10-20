"""
Forex Price Prediction Model
Uses technical indicators and machine learning for price direction prediction
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings
import xgboost as xgb
from tensorflow import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping


class ForexPredictor:
    """
    Forex price direction predictor using ensemble machine learning models
    Predicts whether price will go UP, DOWN, or SIDEWAYS
    """

    def __init__(self):
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.gb_model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        self.xgb_model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric='mlogloss',
            use_label_encoder=False
        )
        self.lstm_model = None  # Will be built during training
        self.lstm_scaler = StandardScaler()  # Separate scaler for LSTM
        self.scaler = StandardScaler()
        self.is_trained = False
        self.lstm_trained = False
        self.sequence_length = 10

    def prepare_features(self, df, indicators):
        """
        Prepare features from price data and indicators

        Args:
            df: DataFrame with OHLCV data
            indicators: Dictionary of technical indicators

        Returns:
            numpy array of features
        """
        features = []

        # Price-based features
        if len(df) > 0:
            current_close = df['close'].iloc[-1]

            # Price momentum features
            if len(df) >= 5:
                features.append(df['close'].pct_change(1).iloc[-1])  # 1-period return
                features.append(df['close'].pct_change(5).iloc[-1])  # 5-period return
                features.append(df['close'].pct_change(10).iloc[-1])  # 10-period return
            else:
                features.extend([0, 0, 0])

            # Volatility features
            if len(df) >= 20:
                features.append(df['close'].pct_change().rolling(20).std().iloc[-1])  # 20-period volatility
            else:
                features.append(0)

            # Volume features
            if 'volume' in df.columns and len(df) >= 5:
                avg_volume = df['volume'].rolling(20).mean().iloc[-1]
                current_volume = df['volume'].iloc[-1]
                features.append(current_volume / avg_volume if avg_volume > 0 else 1)  # Volume ratio
            else:
                features.append(1)
        else:
            features.extend([0, 0, 0, 0, 1])

        # Technical indicator features (handle None values)
        # Must match _calculate_historical_features - 12 features total
        rsi = indicators.get('rsi', 50)
        features.append((rsi if rsi is not None else 50) / 100)  # Feature 6: Normalize RSI

        # Moving averages (4 features)
        current_price = df['close'].iloc[-1] if len(df) > 0 else 0
        features.append(indicators.get('sma_20') or current_price)  # Feature 7
        features.append(indicators.get('sma_50') or current_price)  # Feature 8
        features.append(indicators.get('ema_12') or current_price)  # Feature 9
        features.append(indicators.get('ema_26') or current_price)  # Feature 10

        # Bollinger Bands (3 features)
        features.append(indicators.get('bb_upper') or current_price)  # Feature 11
        features.append(indicators.get('bb_middle') or current_price)  # Feature 12
        features.append(indicators.get('bb_lower') or current_price)  # Feature 13

        # Stochastic (2 features)
        stoch_k = indicators.get('stoch_k', 50)
        stoch_d = indicators.get('stoch_d', 50)
        features.append((stoch_k if stoch_k is not None else 50) / 100)  # Feature 14
        features.append((stoch_d if stoch_d is not None else 50) / 100)  # Feature 15

        # ADX (1 feature)
        adx = indicators.get('adx', 0)
        features.append((adx if adx is not None else 0) / 100)  # Feature 16

        # ATR (1 feature)
        atr = indicators.get('atr', 0)
        features.append(atr if atr is not None else 0)  # Feature 17

        return np.array(features).reshape(1, -1)

    def create_training_data(self, df, indicators_history):
        """
        Create training data from historical price data

        Args:
            df: DataFrame with historical OHLCV data
            indicators_history: List of indicator dictionaries for each period

        Returns:
            X (features), y (labels)
        """
        X = []
        y = []

        # Need at least 30 periods for meaningful training
        if len(df) < 30:
            return None, None

        # Create features for each historical point
        for i in range(20, len(df) - 5):  # Leave room for forward-looking labels
            hist_df = df.iloc[:i+1]

            # Calculate indicators for this historical point
            try:
                features = self._calculate_historical_features(hist_df)

                # Label: price direction 5 periods ahead
                future_price = df['close'].iloc[i + 5]
                current_price = df['close'].iloc[i]
                price_change = (future_price - current_price) / current_price

                # Classify into UP (1), DOWN (0), SIDEWAYS (2)
                if price_change > 0.002:  # > 0.2% move up
                    label = 1  # UP
                elif price_change < -0.002:  # > 0.2% move down
                    label = 0  # DOWN
                else:
                    label = 2  # SIDEWAYS

                X.append(features)
                y.append(label)
            except:
                continue

        if len(X) == 0:
            return None, None

        return np.array(X), np.array(y)

    def _calculate_historical_features(self, df):
        """Calculate features for historical data point"""
        features = []

        # Price momentum
        if len(df) >= 10:
            features.append(df['close'].pct_change(1).iloc[-1])
            features.append(df['close'].pct_change(5).iloc[-1])
            features.append(df['close'].pct_change(10).iloc[-1])
            features.append(df['close'].pct_change().rolling(20).std().iloc[-1])
        else:
            features.extend([0, 0, 0, 0])

        # Volume
        if 'volume' in df.columns and len(df) >= 20:
            avg_volume = df['volume'].rolling(20).mean().iloc[-1]
            current_volume = df['volume'].iloc[-1]
            features.append(current_volume / avg_volume if avg_volume > 0 else 1)
        else:
            features.append(1)

        # Simple technical indicators
        if len(df) >= 20:
            # RSI approximation
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            features.append(rsi.iloc[-1] / 100 if not np.isnan(rsi.iloc[-1]) else 0.5)

            # Moving averages
            sma_20 = df['close'].rolling(20).mean().iloc[-1]
            features.append(sma_20 if not np.isnan(sma_20) else df['close'].iloc[-1])

            sma_50 = df['close'].rolling(50).mean().iloc[-1] if len(df) >= 50 else sma_20
            features.append(sma_50 if not np.isnan(sma_50) else df['close'].iloc[-1])

            ema_12 = df['close'].ewm(span=12).mean().iloc[-1]
            features.append(ema_12 if not np.isnan(ema_12) else df['close'].iloc[-1])

            ema_26 = df['close'].ewm(span=26).mean().iloc[-1]
            features.append(ema_26 if not np.isnan(ema_26) else df['close'].iloc[-1])

            # Bollinger Bands
            bb_middle = df['close'].rolling(20).mean().iloc[-1]
            bb_std = df['close'].rolling(20).std().iloc[-1]
            features.append(bb_middle + 2 * bb_std if not np.isnan(bb_std) else df['close'].iloc[-1])
            features.append(bb_middle if not np.isnan(bb_middle) else df['close'].iloc[-1])
            features.append(bb_middle - 2 * bb_std if not np.isnan(bb_std) else df['close'].iloc[-1])

            # Stochastic (simplified)
            low_14 = df['low'].rolling(14).min().iloc[-1]
            high_14 = df['high'].rolling(14).max().iloc[-1]
            stoch_k = ((df['close'].iloc[-1] - low_14) / (high_14 - low_14)) if (high_14 - low_14) > 0 else 0.5
            features.append(stoch_k)
            features.append(stoch_k)  # Use same value for D

            # ADX approximation (simplified)
            features.append(0.5)

            # ATR
            high_low = df['high'] - df['low']
            atr = high_low.rolling(14).mean().iloc[-1]
            features.append(atr if not np.isnan(atr) else 0)
        else:
            # Not enough data, use defaults
            features.extend([0.5] + [df['close'].iloc[-1]] * 7 + [0.5, 0.5, 0.5, 0])

        return features

    def _build_lstm_model(self, input_shape, num_classes):
        """Build LSTM neural network model"""
        model = Sequential([
            LSTM(64, input_shape=input_shape, return_sequences=True),
            Dropout(0.2),
            LSTM(32, return_sequences=False),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(num_classes, activation='softmax')
        ])
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    def _prepare_lstm_sequences(self, X, sequence_length=10):
        """Prepare sequences for LSTM input"""
        if len(X) < sequence_length:
            return None

        sequences = []
        for i in range(len(X) - sequence_length + 1):
            sequences.append(X[i:i+sequence_length])
        return np.array(sequences)

    def train(self, df):
        """
        Train the prediction models

        Args:
            df: DataFrame with historical OHLCV data

        Returns:
            bool: True if training successful
        """
        X, y = self.create_training_data(df, None)

        if X is None or len(X) < 20:
            return False

        try:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )

            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            # Train traditional models
            self.rf_model.fit(X_train_scaled, y_train)
            self.gb_model.fit(X_train_scaled, y_train)
            self.xgb_model.fit(X_train_scaled, y_train)

            # Calculate accuracies
            rf_accuracy = self.rf_model.score(X_test_scaled, y_test)
            gb_accuracy = self.gb_model.score(X_test_scaled, y_test)
            xgb_accuracy = self.xgb_model.score(X_test_scaled, y_test)

            self.is_trained = True

            # Train LSTM model
            try:
                # Prepare sequences for LSTM
                X_train_lstm_scaled = self.lstm_scaler.fit_transform(X_train)
                X_test_lstm_scaled = self.lstm_scaler.transform(X_test)

                # Create sequences
                X_train_sequences = self._prepare_lstm_sequences(X_train_lstm_scaled, self.sequence_length)
                X_test_sequences = self._prepare_lstm_sequences(X_test_lstm_scaled, self.sequence_length)

                if X_train_sequences is not None and len(X_train_sequences) > 10:
                    # Adjust labels to match sequence data
                    y_train_seq = y_train[self.sequence_length - 1:]
                    y_test_seq = y_test[self.sequence_length - 1:]

                    # Get number of classes
                    num_classes = len(np.unique(y))

                    # Build LSTM model
                    input_shape = (self.sequence_length, X_train.shape[1])
                    self.lstm_model = self._build_lstm_model(input_shape, num_classes)

                    # Early stopping callback
                    early_stop = EarlyStopping(
                        monitor='val_loss',
                        patience=5,
                        restore_best_weights=True,
                        verbose=0
                    )

                    # Train LSTM
                    self.lstm_model.fit(
                        X_train_sequences, y_train_seq,
                        epochs=50,
                        batch_size=32,
                        validation_split=0.2,
                        callbacks=[early_stop],
                        verbose=0
                    )

                    self.lstm_trained = True
                else:
                    print("Not enough data for LSTM sequences, using 3-model ensemble")
                    self.lstm_trained = False

            except Exception as e:
                print(f"LSTM training failed, falling back to 3-model ensemble: {e}")
                self.lstm_trained = False

            return True
        except Exception as e:
            print(f"Error training models: {e}")
            return False

    def predict(self, df, indicators):
        """
        Predict price direction

        Args:
            df: Current DataFrame with OHLCV data
            indicators: Dictionary of current technical indicators

        Returns:
            Dictionary with prediction results
        """
        # Train model if not already trained
        if not self.is_trained and len(df) >= 30:
            self.train(df)

        # If still not trained, return neutral prediction
        if not self.is_trained:
            return {
                'direction': 'NEUTRAL',
                'confidence': 0.0,
                'probability_up': 0.33,
                'probability_down': 0.33,
                'probability_sideways': 0.34,
                'model_status': 'Insufficient data for ML prediction',
                'recommendation': 'Need more historical data for accurate predictions'
            }

        try:
            # Prepare features
            features = self.prepare_features(df, indicators)
            features_scaled = self.scaler.transform(features)

            # Get predictions from traditional models
            rf_proba = self.rf_model.predict_proba(features_scaled)[0]
            gb_proba = self.gb_model.predict_proba(features_scaled)[0]
            xgb_proba = self.xgb_model.predict_proba(features_scaled)[0]

            # Get LSTM prediction if available
            num_models = 3
            if self.lstm_trained and self.lstm_model is not None:
                try:
                    # Get historical data for LSTM sequence
                    X_full, _ = self.create_training_data(df, None)
                    if X_full is not None and len(X_full) >= self.sequence_length:
                        # Use last sequence_length samples
                        X_recent = X_full[-self.sequence_length:]
                        X_recent_scaled = self.lstm_scaler.transform(X_recent)
                        X_lstm_input = X_recent_scaled.reshape(1, self.sequence_length, -1)

                        # Get LSTM prediction
                        lstm_proba = self.lstm_model.predict(X_lstm_input, verbose=0)[0]

                        # Ensemble: average all 4 model probabilities
                        ensemble_proba = (rf_proba + gb_proba + xgb_proba + lstm_proba) / 4
                        num_models = 4
                    else:
                        # Not enough data for LSTM, use 3 models
                        ensemble_proba = (rf_proba + gb_proba + xgb_proba) / 3
                except Exception as e:
                    print(f"LSTM prediction failed, using 3-model ensemble: {e}")
                    ensemble_proba = (rf_proba + gb_proba + xgb_proba) / 3
            else:
                # LSTM not trained, use 3 models
                ensemble_proba = (rf_proba + gb_proba + xgb_proba) / 3

            # Get class labels (may not always be [0, 1, 2] depending on training data)
            classes = self.rf_model.classes_

            # Map to probabilities
            prob_dict = {cls: prob for cls, prob in zip(classes, ensemble_proba)}
            prob_down = prob_dict.get(0, 0)
            prob_up = prob_dict.get(1, 0)
            prob_sideways = prob_dict.get(2, 0)

            # Determine prediction
            max_prob = max(prob_up, prob_down, prob_sideways)

            if max_prob == prob_up:
                direction = 'BULLISH'
                confidence = prob_up
            elif max_prob == prob_down:
                direction = 'BEARISH'
                confidence = prob_down
            else:
                direction = 'NEUTRAL'
                confidence = prob_sideways

            # Generate recommendation
            if confidence > 0.65:
                strength = 'STRONG'
            elif confidence > 0.55:
                strength = 'MODERATE'
            else:
                strength = 'WEAK'

            recommendation = f"{strength} {direction} signal"

            # Set model status based on number of models used
            if num_models == 4:
                model_status = '4-Model Ensemble (RF, GB, XGB, LSTM)'
            else:
                model_status = '3-Model Ensemble (RF, GB, XGB)'

            return {
                'direction': direction,
                'confidence': float(confidence * 100),
                'probability_up': float(prob_up * 100),
                'probability_down': float(prob_down * 100),
                'probability_sideways': float(prob_sideways * 100),
                'model_status': model_status,
                'recommendation': recommendation,
                'timeframe': '5-period ahead prediction'
            }

        except Exception as e:
            print(f"Error making prediction: {e}")
            return {
                'direction': 'ERROR',
                'confidence': 0.0,
                'probability_up': 0.0,
                'probability_down': 0.0,
                'probability_sideways': 0.0,
                'model_status': f'Prediction error: {str(e)}',
                'recommendation': 'Unable to generate prediction'
            }
