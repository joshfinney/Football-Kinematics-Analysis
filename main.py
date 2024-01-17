import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_and_preprocess_data(filepath):
    df = pd.read_csv(filepath, skiprows=3)
    df.columns = [col.strip().replace(' ', '_') for col in df.columns]
    numeric_cols = ['TIME', 'Thigh_Ang_Vel', 'Shank_Ang_Vel', 'TIME.1', 'Thigh_Angle', 'Shank_Ang_Vel.1']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df.dropna(subset=numeric_cols, inplace=True)
    return df

def split_kickers_data(df):
    kicker1 = df[['TIME', 'Thigh_Ang_Vel', 'Shank_Ang_Vel']].copy()
    kicker1.columns = ['TIME', 'Thigh_Ang_Vel_Kicker1', 'Shank_Ang_Vel_Kicker1']
    
    kicker2 = df[['TIME.1', 'Thigh_Angle', 'Shank_Ang_Vel.1']].copy()
    kicker2.columns = ['TIME', 'Thigh_Ang_Vel_Kicker2', 'Shank_Ang_Vel_Kicker2']
    
    return kicker1, kicker2

def plot_kinematic_variables(kicker1, kicker2, ball_contact_time):
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

    colors = ['#1f77b4', '#aec7e8', '#2ca02c', '#98df8a']

    ax.plot(kicker1['TIME'], kicker1['Thigh_Ang_Vel_Kicker1'], color=colors[0], label='Kicker 1 - Thigh', linewidth=2)
    ax.plot(kicker1['TIME'], kicker1['Shank_Ang_Vel_Kicker1'], color=colors[1], label='Kicker 1 - Shank', linewidth=2)
    ax.plot(kicker2['TIME'], kicker2['Thigh_Ang_Vel_Kicker2'], color=colors[2], label='Kicker 2 - Thigh', linewidth=2)
    ax.plot(kicker2['TIME'], kicker2['Shank_Ang_Vel_Kicker2'], color=colors[3], label='Kicker 2 - Shank', linewidth=2)

    ax.axvline(ball_contact_time, color='red', linestyle=':', lw=2, label='Ball Contact')

    for kicker, thigh_col, shank_col, thigh_color, shank_color in zip(
        [kicker1, kicker2], 
        ['Thigh_Ang_Vel_Kicker1', 'Thigh_Ang_Vel_Kicker2'], 
        ['Shank_Ang_Vel_Kicker1', 'Shank_Ang_Vel_Kicker2'], 
        [colors[0], colors[2]], 
        [colors[1], colors[3]]):
        
        max_thigh_idx = kicker[thigh_col].idxmax()
        max_shank_idx = kicker[shank_col].idxmax()
        
        ax.plot(kicker['TIME'][max_thigh_idx], kicker[thigh_col][max_thigh_idx], 'o', color=thigh_color)
        ax.plot(kicker['TIME'][max_shank_idx], kicker[shank_col][max_shank_idx], 'o', color=shank_color)

    ax.set_xlabel('Time (s)', fontsize=14)
    ax.set_ylabel('Angular Velocity (deg/s)', fontsize=14)
    ax.set_title('Thigh and Shank Angular Velocities During Football Kick', fontsize=16)
    ax.grid(True)
    ax.legend(fancybox=True, framealpha=0.7, fontsize=12)

    kicker_data = [kicker1, kicker2]
    max_values = pd.DataFrame({
        'Max Thigh Vel (deg/s)': [k['Thigh_Ang_Vel_Kicker' + str(i+1)].max() for i, k in enumerate(kicker_data)],
        'Max Thigh Vel (rad/s)': [k['Thigh_Ang_Vel_Kicker' + str(i+1)].max() * np.pi / 180 for i, k in enumerate(kicker_data)],
        'Max Shank Vel (deg/s)': [k['Shank_Ang_Vel_Kicker' + str(i+1)].max() for i, k in enumerate(kicker_data)],
        'Max Shank Vel (rad/s)': [k['Shank_Ang_Vel_Kicker' + str(i+1)].max() * np.pi / 180 for i, k in enumerate(kicker_data)],
    }, index=['Kicker 1', 'Kicker 2'])

    max_values = max_values.round(2)

    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.size'] = 10

    table = plt.table(cellText=max_values.values, colLabels=max_values.columns, 
                      rowLabels=max_values.index, cellLoc='center', loc='bottom', bbox=[0, -0.5, 1, 0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    plt.subplots_adjust(left=0.2, bottom=0.2, right=0.95, top=0.9)

    plt.savefig('kinematic_variables_plot.svg', format='svg', bbox_inches='tight')
    plt.savefig('kinematic_variables_plot.png', bbox_inches='tight', dpi=300)
    
    plt.show()

if __name__ == "__main__":
    filepath = 'data.csv'
    df = read_and_preprocess_data(filepath)
    kicker1, kicker2 = split_kickers_data(df)
    ball_contact_time = 0.253
    plot_kinematic_variables(kicker1, kicker2, ball_contact_time)