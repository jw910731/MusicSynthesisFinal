const enum ToneState {
    Major,
    Minor
}

function choose<T>(choices: T[]): T {
  const index = Math.floor(Math.random() * choices.length);
  return choices[index];
}

export {
    ToneState, choose
}