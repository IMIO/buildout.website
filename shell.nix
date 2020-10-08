let
  sources = import ./nix/sources.nix;
  pkgs = import sources.nixpkgs {};
  pythonEnv = pkgs.poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    overrides = pkgs.poetry2nix.overrides.withDefaults (
      self: super: {
        requestsexceptions = super.requestsexceptions.overridePythonAttrs (
          oldAttrs: {
            buildInputs = (oldAttrs.buildInputs or []) ++ [
              self.pbr
            ];
          }
        );
        munch = super.munch.overridePythonAttrs (
          oldAttrs: {
            buildInputs = (oldAttrs.buildInputs or []) ++ [
              self.pbr
            ];
          }
        );

      }
    );
  };

in
pkgs.mkShell {
  buildInputs = [
    pythonEnv
    pkgs.gitAndTools.pre-commit
    pkgs.niv
    pkgs.rnix-lsp
    pkgs.python38.pkgs.poetry
    pkgs.docker-compose
    pkgs.python38Packages.python-language-server
  ];
}
