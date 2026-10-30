# build-preflight.md procedure

The inputs are the M, W and P paths stated in the entry file. The external installation path is an option of the installer, not a separate execution role. The build tool, JDK version, additional JDK candidates, cleanup command, device procedure and install prohibition conditions are declared in P's application document `W/../project/build.md`. This document is the common order for carrying out that declaration. If a declaration is missing or empty, do not guess; leave that step as unverified.

## Scope

Apply only before running the build, test and cleanup commands declared in `build.md`. Do not apply it to a change that does not affect the build result, such as a Trivial that changes only documents or wording.

## JDK resolve order

Apply in a project that uses a JVM-based build tool (for example, Gradle or Maven). Choose the first JDK that is usable in the order below.

1. If the `java` command can run in the current shell, choose it as is.
2. If `JAVA_HOME` is not empty and `bin/java` (`bin/java.exe`) under it is executable, choose that JDK.
3. Check only the additional JDK candidate paths declared in `build.md`.

Do not judge success only because a path exists. Resolve is complete only when `java -version` run once with the chosen JDK succeeds. If the current `java` does not run or a candidate check fails, move on to the next item in the order. Limit the candidate search to the list above. Do not look for a JDK with a filesystem-wide scan or a repository-wide search.

For required build verification, check with the build tool's version command (`gradlew --version` for Gradle) that the major version of **the launcher/daemon JVM the build tool actually uses**, not the resolved JDK, equals `JDK major` in `build.md`.

## Devices and emulators

Follow the device procedure only if `build.md` declares one. If none is declared, do not do device or emulator work; if that work is needed, stop only that work with `BLOCKED: device procedure undeclared`. Device check results are not an implementation, merge or completion gate.

## Process/run scope

- If the current `java` is usable, do not change the existing shell environment.
- If you chose a valid `JAVA_HOME` or a declared candidate but `java` is not on the PATH, set `JAVA_HOME` only for the current shell process and prepend its `bin` to the PATH.
- Do not use `setx`, change the registry, edit the shell profile, change permanent system/user environment variables, or edit build configuration files.
- Record the resolve source, the JDK home, and the results of `java -version` and the build tool version in the current agent run context. Do not cache them in repository files or permanent host settings.
- If a later build command runs in a new shell process, inject the same recorded values into that process's environment again. Do not repeat the candidate search and version check in the same agent run.

## No install / download

Do not automatically install or download a JDK, build tool or SDK. If `build.md` separately allows a scope, follow only that scope. The build tool downloading dependencies is the project's normal build behavior and is not part of this prohibition. However, if it fails because that access is blocked, separate it as an environment failure.

## Stop condition

- If the JDK cannot be resolved, do not run the build command; report `BLOCKED: JDK unavailable`.
- If a JDK of the declared version cannot be confirmed for required build verification, stop with `BLOCKED: canonical build JDK unavailable` and record the commands not run.
- Do not record the states above as PASS.

## Conditional diagnostic mode

The exact trigger keyword is `[BUILD-PREFLIGHT-DIAG]`.

- Activate it only when this keyword is in the current work instruction or in the explicit execution input of that run.
- Without the keyword, do not create a diagnostic record, and do not run additional repository-wide searches or repeated commands for diagnostics.
- When activated, merge the preflight execution path of the same agent run into **one** Issue record. If a diagnostic was already recorded in the same run, do not create a duplicate record.

The decision metadata recorded is limited to the current shell type, the JDK resolve source and `java -version` success/failure, the build tool JVM major check result, whether a fallback happened and its cause category, and whether an install/download was attempted. Do not record actual user names, full environment variable values, the full PATH, or API keys/tokens. If a host path is needed, normalize the user-identifying part to a placeholder such as `<user>`.

## Output

- Scope decision
- JDK resolve source: current `java` / `JAVA_HOME` / declared candidate
- Resolved JDK home or executable, `java -version` result
- Whether the build tool JVM major matches the `build.md` declaration
- Whether it is reused in later commands of the same run
- Whether an install/download was attempted
- On failure: `BLOCKED: JDK unavailable` / `BLOCKED: canonical build JDK unavailable` / `BLOCKED: device procedure undeclared`, the candidate categories checked, the commands not run
