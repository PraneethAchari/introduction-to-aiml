from flask import Flask, jsonify
import random

app = Flask(__name__)

class EqualProbabilityPredictor:
    def __init__(self):
        self.predictions = None
        
    def create_predictions(self):
        """Create predictions where top 5 teams have same probability"""
        print("🎯 Creating equal probability predictions...")
        
        # Teams with equal probabilities for top 5
        teams = [
            {'team': 'Brazil', 'wins': 5, 'finals': 7, 'semis': 11, 'win_rate': 0.73},
            {'team': 'Argentina', 'wins': 3, 'finals': 5, 'semis': 8, 'win_rate': 0.68},
            {'team': 'France', 'wins': 2, 'finals': 4, 'semis': 7, 'win_rate': 0.65},
            {'team': 'Germany', 'wins': 4, 'finals': 8, 'semis': 13, 'win_rate': 0.67},
            {'team': 'Spain', 'wins': 1, 'finals': 1, 'semis': 2, 'win_rate': 0.58},
            {'team': 'England', 'wins': 1, 'finals': 1, 'semis': 3, 'win_rate': 0.55},
            {'team': 'Italy', 'wins': 4, 'finals': 6, 'semis': 8, 'win_rate': 0.61},
            {'team': 'Netherlands', 'wins': 0, 'finals': 3, 'semis': 5, 'win_rate': 0.57},
            {'team': 'Portugal', 'wins': 0, 'finals': 0, 'semis': 3, 'win_rate': 0.54},
            {'team': 'Belgium', 'wins': 0, 'finals': 0, 'semis': 1, 'win_rate': 0.52}
        ]
        
        # Assign same probability to top 5 teams
        base_probability = 0.75  # 75% for top 5
        
        predictions = []
        for i, team in enumerate(teams):
            if i < 5:
                # Top 5 teams get same probability
                probability = base_probability
            else:
                # Other teams get decreasing probabilities
                probability = 0.50 - (i - 5) * 0.05
            
            predictions.append({
                'team': team['team'],
                'probability': probability,
                'world_cup_wins': team['wins'],
                'finals_appearances': team['finals'],
                'semi_finals': team['semis'],
                'win_rate': team['win_rate'],
                'performance_summary': self.get_summary(team),
                'rank': i + 1
            })
        
        self.predictions = predictions
        
        # Print results to console
        print("\n🏆 EQUAL PROBABILITY PREDICTIONS 🏆")
        print("=" * 50)
        print("Top 5 Teams - Same 75% Probability:")
        for i, team in enumerate(predictions[:5], 1):
            print(f"{i}. {team['team']}: {team['probability']*100:.1f}%")
        print("=" * 50)
        print("Other Teams:")
        for i, team in enumerate(predictions[5:], 6):
            print(f"{i}. {team['team']}: {team['probability']*100:.1f}%")
        print("=" * 50)
        
        return predictions
    
    def get_summary(self, team):
        """Get performance summary"""
        if team['wins'] > 0:
            return f"🏆 {team['wins']} World Cup wins"
        elif team['finals'] > 0:
            return f"🥈 {team['finals']} final appearances"
        elif team['semis'] > 0:
            return f"🥉 {team['semis']} semi-finals"
        else:
            return "Strong contender"

# Initialize predictor
predictor = EqualProbabilityPredictor()

# HTML content as string - embedded in Python file
HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Equal Probability World Cup Predictor</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: Arial, sans-serif;
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .special-notice {
            background: gold;
            color: black;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
            border: 3px solid orange;
            font-weight: bold;
            font-size: 1.2em;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .equal-group {
            background: linear-gradient(45deg, #e8f5e8, #d4edda);
            border: 3px solid #28a745;
        }
        
        .winner-card {
            background: linear-gradient(45deg, #FFD700, #FFA500);
            color: black;
            border: 3px solid gold;
            text-align: center;
            padding: 30px;
        }
        
        .team-card {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            border-bottom: 1px solid #eee;
            transition: all 0.3s ease;
        }
        
        .team-card:hover {
            background: #f8f9fa;
            transform: translateX(5px);
        }
        
        .equal-team {
            background: #d4edda;
            border-left: 5px solid #28a745;
        }
        
        .probability-bar {
            height: 20px;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            border-radius: 10px;
            margin: 5px 0;
            transition: width 1s ease-in-out;
        }
        
        .equal-probability {
            background: linear-gradient(90deg, #28a745, #20c997);
        }
        
        .badge {
            background: #007bff;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .equal-badge {
            background: #28a745;
        }
        
        .rank-badge {
            background: #6c757d;
            color: white;
            padding: 8px 12px;
            border-radius: 50%;
            min-width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-weight: bold;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #007bff;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .team-info {
            display: flex;
            align-items: center;
            flex: 1;
        }
        
        .team-stats {
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }
        
        .probability-display {
            text-align: right;
            min-width: 120px;
        }
        
        .teams-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .team-box {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 2px solid #28a745;
            transition: transform 0.3s ease;
        }
        
        .team-box:hover {
            transform: translateY(-5px);
        }
        
        .reload-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .reload-btn:hover {
            background: #218838;
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1 style="font-size: 2.5em; margin-bottom: 10px;">⚽ World Cup 2026 Predictor</h1>
            <p style="font-size: 1.2em;">Special Edition: Top 5 Teams Have Equal Probability</p>
        </div>

        <!-- Special Notice -->
        <div class="special-notice">
            🎯 SPECIAL FEATURE: Top 5 Teams All Have 75% Win Probability!
        </div>

        <!-- Equal Probability Group -->
        <div class="card equal-group">
            <h2 style="text-align: center; color: #155724; font-size: 1.8em; margin-bottom: 20px;">
                🏆 TOP 5 TEAMS - EQUAL 75% PROBABILITY
            </h2>
            
            <!-- Winner Display -->
            <div class="winner-card">
                <div id="winner-section">
                    <div class="loading">
                        <div class="spinner"></div>
                        <p style="font-size: 1.1em;">Loading equal probability predictions...</p>
                    </div>
                </div>
            </div>

            <!-- Equal Teams Grid -->
            <div id="equal-teams-section">
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading top 5 teams...</p>
                </div>
            </div>
        </div>

        <!-- All Predictions -->
        <div class="card">
            <h2 style="text-align: center; margin-bottom: 20px; font-size: 1.8em;">📊 Complete Team Predictions</h2>
            <div id="all-predictions">
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading all team predictions...</p>
                </div>
            </div>
        </div>

        <!-- Explanation -->
        <div class="card">
            <h2 style="text-align: center; margin-bottom: 20px; font-size: 1.8em;">🧮 How It Works</h2>
            
            <div style="background: #e3f2fd; border-left: 4px solid #2196F3; padding: 20px; margin: 15px 0; border-radius: 8px;">
                <h3 style="color: #155724; margin-bottom: 15px;">Equal Probability Formula</h3>
                <p style="font-size: 1.1em; margin-bottom: 10px;"><strong>Top 5 Teams: Fixed 75% probability each</strong></p>
                <p style="font-size: 1.1em;">Teams 6-10: Decreasing probabilities (50% down to 30%)</p>
            </div>

            <div style="text-align: center; margin-top: 30px;">
                <button onclick="loadPredictions()" class="reload-btn">
                    🔄 Reload Predictions
                </button>
            </div>
        </div>

        <div style="text-align: center; color: white; margin-top: 40px; padding: 20px;">
            <p style="font-size: 1.1em;">© 2024 Equal Probability World Cup Predictor</p>
        </div>
    </div>

    <script>
        // Function to display predictions
        function displayPredictions(data) {
            const predictions = data.predictions;
            
            // Display winner (first of equal group)
            const winner = predictions[0];
            document.getElementById('winner-section').innerHTML = `
                <h1 style="margin: 0; font-size: 2.8em;">${winner.team}</h1>
                <h2 style="color: #155724; margin: 15px 0; font-size: 2em;">${(winner.probability * 100).toFixed(1)}% Win Probability</h2>
                <p style="margin: 10px 0; font-size: 1.2em;">${winner.performance_summary}</p>
                <p style="margin: 8px 0; font-size: 1.1em;">World Cup Wins: ${winner.world_cup_wins} | Finals: ${winner.finals_appearances}</p>
                <div style="background: #155724; color: white; padding: 12px; border-radius: 10px; margin-top: 15px; font-size: 1.1em;">
                    🎯 Part of Top 5 Equal Probability Group
                </div>
            `;

            // Display equal teams grid
            const equalTeams = predictions.slice(0, 5);
            let equalTeamsHTML = '<div class="teams-grid">';
            
            equalTeams.forEach((team, index) => {
                equalTeamsHTML += `
                    <div class="team-box">
                        <div style="font-size: 1.3em; font-weight: bold; margin-bottom: 10px;">${team.team}</div>
                        <div style="font-size: 1.8em; color: #28a745; font-weight: bold; margin: 15px 0;">${(team.probability * 100).toFixed(1)}%</div>
                        <div style="font-size: 1em; color: #666; margin-bottom: 10px;">${team.performance_summary}</div>
                        <div style="margin-top: 10px;">
                            <span style="background: #28a745; color: white; padding: 5px 12px; border-radius: 15px; font-size: 0.9em; font-weight: bold;">
                                Rank ${index + 1}
                            </span>
                        </div>
                    </div>
                `;
            });
            
            equalTeamsHTML += '</div>';
            document.getElementById('equal-teams-section').innerHTML = equalTeamsHTML;

            // Display all predictions
            let allPredictionsHTML = '';
            predictions.forEach((team, index) => {
                const isEqualGroup = index < 5;
                const probPercent = (team.probability * 100).toFixed(1);
                
                allPredictionsHTML += `
                    <div class="team-card ${isEqualGroup ? 'equal-team' : ''}">
                        <div class="team-info">
                            <div class="rank-badge ${isEqualGroup ? 'equal-badge' : ''}">${index + 1}</div>
                            <div>
                                <strong style="font-size: 1.1em;">${team.team}</strong>
                                <div class="team-stats">
                                    ${team.performance_summary} | Wins: ${team.world_cup_wins} | Finals: ${team.finals_appearances}
                                </div>
                            </div>
                        </div>
                        <div class="probability-display">
                            <div class="badge ${isEqualGroup ? 'equal-badge' : ''}">${probPercent}%</div>
                            <div class="probability-bar ${isEqualGroup ? 'equal-probability' : ''}" style="width: ${probPercent}%"></div>
                            ${isEqualGroup ? '<div style="font-size: 0.8em; color: #28a745; margin-top: 5px; font-weight: bold;">Equal Group</div>' : ''}
                        </div>
                    </div>
                `;
            });
            
            document.getElementById('all-predictions').innerHTML = allPredictionsHTML;

            // Animate probability bars
            setTimeout(() => {
                document.querySelectorAll('.probability-bar').forEach(bar => {
                    bar.style.width = bar.style.width;
                });
            }, 100);
        }

        // Load predictions from API
        function loadPredictions() {
            // Show loading states
            document.getElementById('winner-section').innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading equal probability predictions...</p>
                </div>
            `;
            
            document.getElementById('equal-teams-section').innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading top 5 teams...</p>
                </div>
            `;
            
            document.getElementById('all-predictions').innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading all team predictions...</p>
                </div>
            `;

            fetch('/api/predictions')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        displayPredictions(data);
                    } else {
                        alert('Error loading predictions: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Network error loading predictions. Please check if the server is running.');
                });
        }

        // Load predictions when page loads
        document.addEventListener('DOMContentLoaded', loadPredictions);
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    """Main page route - serves HTML directly"""
    try:
        if predictor.predictions is None:
            predictor.create_predictions()
        return HTML_CONTENT
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"

@app.route('/api/predictions')
def get_predictions():
    """API endpoint to get predictions"""
    try:
        if predictor.predictions is None:
            predictor.create_predictions()
        
        return jsonify({
            'success': True,
            'predictions': predictor.predictions,
            'total_teams': len(predictor.predictions),
            'special_note': 'Top 5 teams have equal 75% probability'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🚀 Starting Equal Probability World Cup Predictor")
    print("=" * 60)
    print("SPECIAL: Top 5 teams have SAME win probability (75%)")
    print("=" * 60)
    
    # Create predictions
    predictor.create_predictions()
    
    print("🌐 Starting web server...")
    print("📱 Open: http://127.0.0.1:5000")
    print("⏹️  Press Ctrl+C to stop")
    
    # Run Flask app
    app.run(debug=True, host='127.0.0.1', port=5000)