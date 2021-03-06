from CONST import ASSETS_FOLDER

data = [

  [ # Puzzle 1:
    { # Success condition 1:
      "objectId": 1,
      "preset": 0,
      "tolerance": [
        1,
        1,
        1,
        1
      ],
      "values": [
        0,
        0,
        0,
        0
      ]
    }
  ],

  [ # Puzzle 2 :
    { # Success condition 1:
      "objectId": 1,
      "preset": 0,
      "tolerance": [
        0,
        0,
        0,
        0
      ],
      "values": [
        0,
        0,
        0,
        1
      ]
    }
  ],

  [ # Puzzle 3 :
    { # Success condition 1:
      "objectId": 1,
      "preset": 0,
      "tolerance": [
        0,
        0,
        0,
        0
      ],
      "values": [
        1,
        0,
        0,
        0
      ]
    }
  ],

  [ # Puzzle 4 :
    { # Success condition 1:
      "objectId": 0,
      "preset": 0,
      "tolerance": [
        1.0,
        1.0,
        1.0
      ],
      "values": [
        0.5,
        0.5,
        0.0
      ]
    }
  ],

  [ # Puzzle 5 :
    { # Success condition 1:
      "objectId": 0,
      "preset": 0,
      "tolerance": [
        1.0,
        0.2,
        1.0
      ],
      "values": [
        0.5,
        0.84,
        0.0
      ]
    }
  ],

  [ # Puzzle 6 :
    { # Success condition 1:
      "objectId": 0,
      "preset": 0,
      "tolerance": [
        1.0,
        0.2,
        1.0
      ],
      "values": [
        0.50,
        0.24,
        0.0
      ]
    }
  ],

  [ # Puzzle 7 :
    { # Success condition 1:
      "objectId": 3,
      "preset": 0,
      "tolerance": [
        1.0,
        1.0,
        1.0
      ],
      "values": [
        0,
        0,
        0,
      ]
    }
  ],

  [ # Puzzle 8 :
    { # Success condition 1:
      "objectId": 3,
      "preset": 0,
      "tolerance": [
        0.2,
        0.2,
        0.2
      ],
      "values": [
        1.0,
        0,
        0
      ]
    }
  ],

  [ # Puzzle 9 :
    { # Success condition 1:
      "objectId": 3,
      "preset": 0,
      "tolerance": [
        0.2,
        0.2,
        0.2
      ],
      "values": [
        0.0,
        1.0,
        0.0
      ]
    }
  ],

  [ # Puzzle 10 :
    { # Success condition 1:
      "objectId": 3,
      "preset": 0,
      "tolerance": [
        0.2,
        0.2,
        0.3
      ],
      "values": [
        0.0,
        0.0,
        1.0
      ]
    }
  ],

  [ # Puzzle 11 :
    { # Success condition 1:
      "objectId": 2,
      "preset": 0,
      "tolerance": [
        1,
        1,
        1
      ],
      "values": [
        0.5,
        0.5,
        0
      ]
    }
  ],

  [ # Puzzle 12 :
    { # Success condition 1:
      "objectId": 2,
      "preset": 0,
      "tolerance": [
        1,
        1,
        0.4
      ],
      "values": [
        0.5,
        0.5,
        0.5
      ]
    }
  ],

  [ # Puzzle 13 :
    { # Success condition 1:
      "objectId": 2,
      "preset": 0,
      "tolerance": [
        0.2,
        1.0,
        1
      ],
      "values": [
        0.9,
        0.9,
        0
      ]
    }
  ]

] # end


INSTRUCTIONS_FOLDER = ASSETS_FOLDER + '/audio/instructions/'

# Path for instructions
paths = [
  INSTRUCTIONS_FOLDER + '00_ocarina00.WAV', # level1
  INSTRUCTIONS_FOLDER + '01_ocarina01.WAV', # level2
  INSTRUCTIONS_FOLDER + '000_generique_aToiDeJouer.WAV', # level3
  INSTRUCTIONS_FOLDER + '000_generique_trouveInstrumentClique.WAV', # level4
  INSTRUCTIONS_FOLDER + '000_generique_aToiDeJouer.WAV', # level5
  INSTRUCTIONS_FOLDER + '000_generique_aTonTour.WAV', # level6
  INSTRUCTIONS_FOLDER + '000_generique_trouveInstrumentClique.WAV', # level7
  INSTRUCTIONS_FOLDER + '000_generique_aTonTour.WAV', # level8
  INSTRUCTIONS_FOLDER + '000_generique_aToiDeJouer.WAV', # level9
  INSTRUCTIONS_FOLDER + '000_generique_aTonTour.WAV', # level10
  INSTRUCTIONS_FOLDER + '000_generique_trouveInstrumentClique.WAV', # level11
  INSTRUCTIONS_FOLDER + '000_generique_aToiDeJouer.WAV', # level12
  INSTRUCTIONS_FOLDER + '000_generique_aTonTour.WAV', # level13


]