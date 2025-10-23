{
  description = "Data analysis project with Python and SQLite";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Python and packages
            python3
            python3Packages.numpy
            python3Packages.pandas
            python3Packages.scipy
            python3Packages.matplotlib
            python3Packages.seaborn
            python3Packages.plotly
            python3Packages.jupyter
            python3Packages.scikit-learn

            # slides
            marp-cli

            # Database
            sqlite

            # Shell
            zsh

            # Additional tools
            git
            curl
            wget
          ];

          shellHook = ''
            echo "Welcome to your data analysis development environment!"
            export SHELL=/bin/zsh
            exec zsh
          '';
        };
      });
}
